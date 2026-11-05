(function () {
  "use strict";

  var STORAGE_PREFIX = "magic-maid.pv-manual-review.v1:";
  var STATUSES = Object.freeze({
    pending: "待评审", approved: "人工通过", rework: "需要返修",
    hold: "暂缓判断", skip: "跳过"
  });
  function text(value) {
    if (value === null || value === undefined) return "";
    return typeof value === "object" ? JSON.stringify(value) : String(value);
  }
  function normaliseItems(data) {
    var source = data && Array.isArray(data.items) ? data.items : [];
    return source.map(function (entry, index) {
      var item = entry && typeof entry === "object" ? entry : {};
      return Object.assign({}, item, {
        id: text(item.id).trim() || "未命名条目-" + (index + 1),
        group: text(item.group).trim() || "未分组",
        section: text(item.section),
        production_status: text(item.production_status) || "未提供"
      });
    });
  }
  function imageIdentity(version) {
    var hash = text(version.image_sha256).trim().toLowerCase();
    return hash || "unhashed:" + (text(version.image_path) || text(version.image_url) || "no-image");
  }
  function recordKey(id, version) {
    return STORAGE_PREFIX + encodeURIComponent(id) + ":" + encodeURIComponent(imageIdentity(version));
  }
  function versionsFor(item) {
    var current = {
      label: "当前图" + (item.version ? " · " + text(item.version) : ""),
      image_url: item.image_url, white_url: item.white_url, black_url: item.black_url,
      image_path: item.image_path, image_sha256: item.image_sha256, is_current: true
    };
    var versions = [current], seen = new Set([imageIdentity(current)]);
    (Array.isArray(item.versions) ? item.versions : []).forEach(function (entry, index) {
      if (!entry || typeof entry !== "object") return;
      var key = imageIdentity(entry);
      if (seen.has(key)) return;
      seen.add(key);
      versions.push(Object.assign({}, entry, {
        label: text(entry.label) || "历史版本 " + (index + 1), is_current: false
      }));
    });
    return versions;
  }
  function normaliseRecord(item, version, stored) {
    var value = stored && typeof stored === "object" ? stored : {};
    return {
      id: item.id,
      image_sha256: text(version.image_sha256).trim().toLowerCase(),
      image_path: text(version.image_path),
      image_identity: imageIdentity(version),
      status: Object.prototype.hasOwnProperty.call(STATUSES, value.status) ? value.status : "pending",
      note: typeof value.note === "string" ? value.note : "",
      updated_at: typeof value.updated_at === "string" ? value.updated_at : null
    };
  }
  function countsFor(items, lookup) {
    var result = { total: items.length, pending: 0, approved: 0, rework: 0, hold: 0, skip: 0 };
    items.forEach(function (item) {
      var record = lookup(item, versionsFor(item)[0]);
      result[record.status] += 1;
    });
    result.reviewed = result.total - result.pending;
    return result;
  }
  function buildExport(data, items, lookup, storedRecords, timestamp) {
    var includedKeys = new Set();
    var exportedItems = items.map(function (item) {
      var versions = versionsFor(item);
      var records = versions.map(function (version) {
        includedKeys.add(recordKey(item.id, version));
        return Object.assign({}, lookup(item, version), {
          version_label: version.label, is_current: version.is_current
        });
      });
      return Object.assign({}, item, {
        manual_status: records[0].status,
        manual_note: records[0].note,
        manual_review: records[0],
        version_reviews: records
      });
    });
    return {
      schema: "pv-human-manual-review-export/v1",
      exported_at: timestamp || new Date().toISOString(),
      source_schema: data.schema || null,
      dataset_generated_at: data.generated_at || null,
      declared_dataset_total: data.total === undefined ? null : data.total,
      total: exportedItems.length,
      requirements: data.requirements || null,
      scope: {
        review_type: "human_manual_static_artwork",
        current_image_counts_only: true,
        machine_status_is_not_manual_approval: true,
        original_assets_modified: false,
        production_registry_or_bindings_modified: false,
        playback_or_dynamic_validation: false
      },
      counts: countsFor(items, lookup),
      items: exportedItems,
      additional_local_reviews: (storedRecords || []).filter(function (entry) {
        return !includedKeys.has(entry.key);
      }).map(function (entry) { return Object.assign({}, entry.record); })
    };
  }

  // Pure data functions also permit offline Node validation without a browser.
  if (typeof document === "undefined") {
    if (typeof module !== "undefined" && module.exports) {
      module.exports = { normaliseItems: normaliseItems, versionsFor: versionsFor,
        recordKey: recordKey, normaliseRecord: normaliseRecord, countsFor: countsFor,
        buildExport: buildExport, STATUSES: STATUSES };
    }
    return;
  }

  var data = window.PV_REVIEW_DATA && typeof window.PV_REVIEW_DATA === "object"
    ? window.PV_REVIEW_DATA : {};
  var items = normaliseItems(data);
  var byId = new Map(items.map(function (item) { return [item.id, item]; }));
  var versionsById = new Map(items.map(function (item) { return [item.id, versionsFor(item)]; }));
  var records = new Map();
  var selectedVersions = new Map();
  var selectedId = items.length ? items[0].id : null;
  var background = "white", filtered = items.slice();
  var storageAvailable = true, storageIssue = "", malformedRecords = 0;
  var el = {};
  [
    "export-button", "storage-warning", "data-warning", "total-count", "pending-count",
    "approved-count", "rework-count", "progress-label", "review-progress", "other-counts",
    "requirements-panel", "requirements-content", "search-input", "group-filter",
    "status-filter", "filter-count", "clear-filters", "list-count", "item-list",
    "list-empty", "detail-panel", "detail-group", "detail-title", "detail-source-meta",
    "previous-item", "next-item", "navigation-position", "outside-filter", "version-select",
    "background-buttons", "historical-notice", "source-open", "drawing-open",
    "source-image-host", "drawing-image-host", "drawing-caption", "production-status",
    "image-hash", "warnings-panel", "warnings-summary", "warnings-list", "save-status",
    "manual-status-buttons", "review-note", "source-path", "drawing-path", "full-hash",
    "welcome-panel", "dataset-meta", "export-status"
  ].forEach(function (id) { el[id] = document.getElementById(id); });

  function showStorageIssue(message) {
    el["storage-warning"].hidden = !message;
    el["storage-warning"].textContent = message;
  }
  function readStorage() {
    try {
      var store = window.localStorage;
      for (var i = 0; i < store.length; i += 1) {
        var key = store.key(i);
        if (!key || !key.startsWith(STORAGE_PREFIX)) continue;
        try {
          var value = JSON.parse(store.getItem(key));
          if (!value || typeof value.id !== "string" ||
              typeof value.image_identity !== "string") {
            malformedRecords += 1; continue;
          }
          records.set(key, value);
        } catch (_) { malformedRecords += 1; }
      }
    } catch (_) {
      storageAvailable = false;
      storageIssue = "浏览器无法读取本地存储。本页仍可评审与导出，但请在关闭页面前导出 JSON。";
    }
    if (malformedRecords) {
      storageIssue += (storageIssue ? " " : "") + "另有 " + malformedRecords +
        " 条本地记录无法读取，原记录未改写。";
    }
    showStorageIssue(storageIssue);
  }
  function lookup(item, version) {
    var key = recordKey(item.id, version), value = records.get(key);
    if (value && (value.id !== item.id || value.image_identity !== imageIdentity(version))) value = null;
    return normaliseRecord(item, version, value);
  }
  function currentItem() { return byId.get(selectedId) || null; }
  function currentVersion() {
    var versions = versionsById.get(selectedId) || [];
    return versions[selectedVersions.get(selectedId) || 0] || versions[0] || null;
  }
  function safeURL(value) {
    if (!value || typeof value !== "string") return null;
    try {
      var url = new URL(value, window.location.href);
      if (url.protocol === "file:" && window.location.protocol === "file:") return url.href;
      if ((url.protocol === "http:" || url.protocol === "https:") &&
          url.origin === window.location.origin) return url.href;
    } catch (_) { /* An invalid URL is an unavailable image, not markup. */ }
    return null;
  }
  function imageURL(version, bg) {
    if (bg === "black") return version.black_url || version.image_url || version.white_url;
    if (bg === "white") return version.white_url || version.image_url || version.black_url;
    return version.image_url || version.white_url || version.black_url;
  }
  function placeholder(message) {
    var node = document.createElement("p");
    node.className = "image-placeholder";
    node.textContent = message;
    return node;
  }
  function renderImage(host, rawURL, alt, lazy) {
    var url = safeURL(rawURL);
    host.replaceChildren();
    if (!url) {
      host.append(placeholder("暂无可读取的图片"));
      return;
    }
    var img = document.createElement("img");
    img.alt = alt; img.loading = lazy ? "lazy" : "eager"; img.decoding = "async";
    img.addEventListener("error", function () {
      if (host.contains(img)) host.replaceChildren(placeholder("图片未找到或无法读取，请检查文件路径。"));
    });
    img.src = url; host.append(img);
  }
  function setLink(anchor, value) {
    var url = safeURL(value);
    anchor.hidden = !url;
    if (url) anchor.href = url;
    else anchor.removeAttribute("href");
  }
  function renderCounts() {
    var counts = countsFor(items, lookup);
    el["total-count"].textContent = counts.total;
    el["pending-count"].textContent = counts.pending;
    el["approved-count"].textContent = counts.approved;
    el["rework-count"].textContent = counts.rework;
    el["other-counts"].textContent = "暂缓 " + counts.hold + " · 跳过 " + counts.skip;
    el["progress-label"].textContent = "已记录状态 " + counts.reviewed + " / " + counts.total;
    el["review-progress"].max = Math.max(counts.total, 1);
    el["review-progress"].value = counts.reviewed;
    Array.from(el["status-filter"].options).forEach(function (option) {
      if (option.value) option.textContent = STATUSES[option.value] + "（" + counts[option.value] + "）";
    });
  }
  function searchText(item) {
    var versions = versionsById.get(item.id);
    return [item.id, item.group, item.section, item.source_frame, item.production_status,
      item.version, item.image_path].concat(versions.map(function (version) {
        return version.label + " " + lookup(item, version).note;
      })).map(text).join(" ").toLocaleLowerCase();
  }
  function applyFilters() {
    var group = el["group-filter"].value, status = el["status-filter"].value;
    var query = el["search-input"].value.trim().toLocaleLowerCase();
    filtered = items.filter(function (item) {
      return (!group || item.group === group) &&
        (!status || lookup(item, versionsById.get(item.id)[0]).status === status) &&
        (!query || searchText(item).includes(query));
    });
    renderList();
    renderNavigation();
  }
  function renderList() {
    var fragment = document.createDocumentFragment();
    filtered.forEach(function (item) {
      var version = versionsById.get(item.id)[0], record = lookup(item, version);
      var row = document.createElement("button");
      row.type = "button"; row.className = "item-row"; row.dataset.itemId = item.id;
      row.setAttribute("aria-current", item.id === selectedId ? "true" : "false");
      row.setAttribute("aria-label", item.id + "，" + STATUSES[record.status]);
      var thumb = document.createElement("span"); thumb.className = "thumbnail";
      var url = safeURL(version.white_url || version.image_url || version.black_url);
      if (url) {
        var img = document.createElement("img");
        img.loading = "lazy"; img.decoding = "async"; img.alt = "";
        img.addEventListener("error", function () { thumb.textContent = "无图"; });
        img.src = url; thumb.append(img);
      } else thumb.textContent = "未出图";
      var copy = document.createElement("span"); copy.className = "item-copy";
      var title = document.createElement("span"); title.className = "item-id"; title.textContent = item.id;
      var meta = document.createElement("span"); meta.className = "item-meta";
      meta.textContent = item.group + (item.source_frame !== undefined ? " · F" + item.source_frame : "");
      var badge = document.createElement("span");
      badge.className = "status-chip status-" + record.status; badge.textContent = STATUSES[record.status];
      copy.append(title, meta, badge); row.append(thumb, copy); fragment.append(row);
    });
    el["item-list"].replaceChildren(fragment);
    el["filter-count"].textContent = "匹配 " + filtered.length + " 项";
    el["list-count"].textContent = filtered.length + " / " + items.length;
    el["list-empty"].hidden = filtered.length !== 0;
  }
  function renderNavigation() {
    var index = filtered.findIndex(function (item) { return item.id === selectedId; });
    el["navigation-position"].textContent = index >= 0 ? (index + 1) + " / " + filtered.length : "筛选外";
    el["previous-item"].disabled = !filtered.length || index <= 0;
    el["next-item"].disabled = !filtered.length || index === filtered.length - 1;
    el["outside-filter"].hidden = !selectedId || index >= 0;
  }
  function selectItem(id) {
    if (!byId.has(id)) return;
    selectedId = id; renderList(); renderDetail();
  }
  function moveItem(direction) {
    if (!filtered.length) return;
    var index = filtered.findIndex(function (item) { return item.id === selectedId; });
    var next = index < 0 ? 0 : index + direction;
    if (next >= 0 && next < filtered.length) selectItem(filtered[next].id);
  }
  function showSaveStatus(record, justSaved) {
    var message = "尚未人工记录";
    if (record.updated_at) {
      var stamp = new Date(record.updated_at);
      message = (justSaved ? "已保存 " : "本机记录 ") +
        (Number.isNaN(stamp.getTime()) ? record.updated_at : stamp.toLocaleTimeString("zh-CN"));
    }
    if (!storageAvailable && record.updated_at) message = "仅保留在本页，请导出";
    el["save-status"].textContent = message;
    el["save-status"].classList.toggle("unsaved", !storageAvailable && !!record.updated_at);
  }
  function renderManual(record) {
    Array.from(el["manual-status-buttons"].querySelectorAll("button")).forEach(function (button) {
      button.setAttribute("aria-pressed", button.dataset.status === record.status ? "true" : "false");
      button.disabled = button.dataset.status === "approved" && !safeURL(imageURL(currentVersion(), background));
      button.title = button.disabled ? "此版本暂无可读取的绘制图" : "";
    });
    el["review-note"].value = record.note;
    showSaveStatus(record, false);
  }
  function renderDrawing() {
    var item = currentItem(), version = currentVersion();
    if (!item || !version) return;
    var labels = { white: "白底", black: "黑底", transparent: "透明格" };
    var rawURL = imageURL(version, background);
    var exact = background === "white" ? (version.white_url || version.image_url) :
      background === "black" ? (version.black_url || version.image_url) : version.image_url;
    el["drawing-caption"].textContent = "绘制图 · " + labels[background] + (exact ? "" : "（备用合成预览）");
    el["drawing-image-host"].className = "image-host background-" + background;
    renderImage(el["drawing-image-host"], rawURL, item.id + " · " + version.label, false);
    setLink(el["drawing-open"], rawURL);
    Array.from(el["background-buttons"].querySelectorAll("button")).forEach(function (button) {
      button.setAttribute("aria-pressed", button.dataset.background === background ? "true" : "false");
    });
  }
  function renderDetail() {
    var item = currentItem();
    el["detail-panel"].hidden = !item;
    el["welcome-panel"].hidden = !!item;
    if (!item) return;
    var versions = versionsById.get(item.id), version = currentVersion();
    el["detail-title"].textContent = item.id;
    el["detail-group"].textContent = item.group + (item.section ? " / " + item.section : "");
    el["detail-source-meta"].textContent = (item.source_frame === undefined ? "原帧未提供" : "原帧 F" + item.source_frame) +
      " · PTS " + (item.source_pts === undefined ? "未提供" : item.source_pts) +
      " · 时间基 " + (item.source_time_base || "未提供");
    el["version-select"].replaceChildren();
    versions.forEach(function (entry, index) {
      var option = document.createElement("option");
      option.value = String(index); option.textContent = entry.label +
        (entry.image_sha256 ? " · " + text(entry.image_sha256).slice(0, 10) : " · 无 SHA");
      el["version-select"].append(option);
    });
    el["version-select"].value = String(selectedVersions.get(item.id) || 0);
    el["version-select"].disabled = versions.length < 2;
    el["historical-notice"].hidden = version.is_current;
    renderImage(el["source-image-host"], item.source_url, item.id + " 原 PV", false);
    setLink(el["source-open"], item.source_url);
    renderDrawing();
    el["production-status"].textContent = item.production_status;
    el["image-hash"].textContent = version.image_sha256 ? "SHA " + text(version.image_sha256).slice(0, 16) + "…" : "未提供图片 SHA";
    el["source-path"].textContent = text(item.source_path) || "未提供";
    el["drawing-path"].textContent = text(version.image_path) || "未提供";
    el["full-hash"].textContent = text(version.image_sha256) || "无 SHA：使用本版本路径隔离记录";
    var warnings = item.review_warnings;
    if (!Array.isArray(warnings)) warnings = warnings ? [warnings] : [];
    el["warnings-panel"].hidden = !warnings.length;
    el["warnings-summary"].textContent = "已有机审／生产提示（" + warnings.length + "）";
    el["warnings-list"].replaceChildren();
    warnings.forEach(function (warning) {
      var li = document.createElement("li"); li.textContent = text(warning); el["warnings-list"].append(li);
    });
    renderManual(lookup(item, version)); renderNavigation();
  }
  function saveReview(changes) {
    var item = currentItem(), version = currentVersion();
    if (!item || !version) return;
    var record = Object.assign({}, lookup(item, version), changes, { updated_at: new Date().toISOString() });
    record = normaliseRecord(item, version, record);
    var key = recordKey(item.id, version); records.set(key, record);
    try {
      window.localStorage.setItem(key, JSON.stringify(record));
      storageAvailable = true;
      if (!malformedRecords) { storageIssue = ""; showStorageIssue(""); }
    } catch (_) {
      storageAvailable = false;
      showStorageIssue("浏览器未能保存记录（可能因权限或空间限制）。本页意见仍在，请在关闭前导出 JSON。");
    }
    showSaveStatus(record, true);
    renderCounts(); applyFilters();
    Array.from(el["manual-status-buttons"].querySelectorAll("button")).forEach(function (button) {
      button.setAttribute("aria-pressed", button.dataset.status === record.status ? "true" : "false");
    });
  }
  function exportReview() {
    var content = buildExport(data, items, lookup, Array.from(records, function (entry) {
      return { key: entry[0], record: entry[1] };
    }));
    var blob = new Blob([JSON.stringify(content, null, 2) + "\n"], { type: "application/json;charset=utf-8" });
    var url = URL.createObjectURL(blob), anchor = document.createElement("a");
    var stamp = new Date().toISOString().replace(/[:.]/g, "-");
    anchor.href = url; anchor.download = "PV_人工评审_" + stamp + ".json";
    document.body.append(anchor); anchor.click(); anchor.remove();
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 30000);
    el["export-status"].textContent = "已导出全部 " + items.length + " 项（含未评项与各版本记录）";
  }

  readStorage();
  var groups = Array.from(new Set(items.map(function (item) { return item.group; })));
  groups.sort(function (a, b) { return a.localeCompare(b, "zh-CN", { numeric: true }); });
  groups.forEach(function (group) {
    var option = document.createElement("option");
    option.value = group;
    option.textContent = group + "（" + items.filter(function (item) { return item.group === group; }).length + "）";
    el["group-filter"].append(option);
  });
  if (data.requirements) {
    el["requirements-panel"].hidden = false;
    el["requirements-content"].textContent = typeof data.requirements === "string"
      ? data.requirements : JSON.stringify(data.requirements, null, 2);
  }
  var problems = [];
  if (data.total !== undefined && Number(data.total) !== items.length) {
    problems.push("数据声明 " + data.total + " 项，实际载入 " + items.length + " 项；导出以全部实际载入条目为准。");
  }
  if (byId.size !== items.length) problems.push("数据存在重复 ID，请检查数据后再评审；同 ID＋同图 SHA 会共用记录。");
  el["data-warning"].hidden = !problems.length;
  el["data-warning"].textContent = problems.join(" ");
  el["dataset-meta"].textContent = (data.generated_at ? "数据生成于 " + data.generated_at + " · " : "") +
    "本地人工意见不修改原图、注册表或曝光绑定。";
  el["export-button"].disabled = !items.length;
  el["search-input"].addEventListener("input", applyFilters);
  el["group-filter"].addEventListener("change", applyFilters);
  el["status-filter"].addEventListener("change", applyFilters);
  el["clear-filters"].addEventListener("click", function () {
    el["search-input"].value = ""; el["group-filter"].value = ""; el["status-filter"].value = ""; applyFilters();
  });
  el["item-list"].addEventListener("click", function (event) {
    var row = event.target.closest("button[data-item-id]");
    if (row) selectItem(row.dataset.itemId);
  });
  el["previous-item"].addEventListener("click", function () { moveItem(-1); });
  el["next-item"].addEventListener("click", function () { moveItem(1); });
  el["version-select"].addEventListener("change", function () {
    selectedVersions.set(selectedId, Number(el["version-select"].value)); renderDetail();
  });
  el["background-buttons"].addEventListener("click", function (event) {
    var button = event.target.closest("button[data-background]");
    if (button) { background = button.dataset.background; renderDrawing(); }
  });
  el["manual-status-buttons"].addEventListener("click", function (event) {
    var button = event.target.closest("button[data-status]");
    if (button && !button.disabled) saveReview({ status: button.dataset.status });
  });
  el["review-note"].addEventListener("input", function () { saveReview({ note: el["review-note"].value }); });
  el["export-button"].addEventListener("click", exportReview);
  renderCounts(); applyFilters(); renderDetail();
}());
