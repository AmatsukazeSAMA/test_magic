from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import hashlib,json
BASE=Path("D:/CODEX/魔术之心/art/full_character_redraw_1080p_v01")
TASK=BASE/"review/prep_s04_pending_source476507_20261102_v01"
read=lambda p:json.loads(p.read_text("utf-8-sig"))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ev=lambda p:{"path":str(p),"sha256":sha(p)}
def save(p,d):
    assert not p.exists(),f"Preserve evidence: {p}"
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
index=read(TASK/"FINAL_PREPARED_INDEX.json")
out=[]
for en in index["entries"]:
    run=Path(en["run"]);q=read(run/"API_PREPARED_REQUEST.json");l=read(run/"REQUEST_LOCK.json")
    preview=read(run/"API_PREVIEW_PROOF_PREPONLY.json")
    guard=read(run/"PREVIEW_GUARD_REFUSAL_PROOF.json")
    for x in [l["prepared_request"],l["draft"],l["prompt"],l["wrapper"],l["authorization"],l["JOB"],l["REGISTRATION_PLAN"],l["source_audit"],l["input_review"],l["requirements"],l["configured_connection_public"],*l["references"]]:
        assert sha(Path(x["path"]))==x["sha256"],x["path"]
    assert preview["model"]=="gpt-image-2.5-sunburst"
    assert preview["endpoint"]=="https://api.openai.com/v1/images/edits"
    assert preview["quality"]=="high" and preview["n"]==1 and preview["background"]=="transparent"
    assert preview["size"]==q["Size"] and preview["input_count"]==5 and not preview["mask_provided"]
    assert preview["submitted"] is False and preview["spatial_prefix_applied"] is True
    assert guard["preview_omitted_refused_before_wrapper"] is True
    assert Path(q["PromptFile"]).read_text("utf-8").startswith(l["mandatory_prefix"])
    refs=read(run/"FIRST_DRAFT_PREPONLY.json")["references"]
    for ref in refs:
        image=Image.open(ref["path"])
        assert list(image.size)==ref["dimensions"]
        src=Image.open(ref["source"])
        deriv=ref["derivation"]
        if deriv=="exact_byte_copy":
            assert sha(Path(ref["path"]))==sha(Path(ref["source"]))
        elif "rectangle_crop" in deriv:
            roi=ref["source_roi_xyxy"]
            expected=src.convert("RGBA").crop(roi)
            if "white_alpha_composite" in deriv:
                canvas=Image.new("RGBA",expected.size,"white");canvas.alpha_composite(expected);expected=canvas.convert("RGB")
            else:expected=src.crop(roi)
            assert image.mode==expected.mode and image.tobytes()==expected.tobytes()
        else:raise RuntimeError(deriv)
    forbidden=["attempt.json","result.json","character_api_original.png","character_imggen_original.png",
      "ROOT_API_EXECUTION_RECEIPT.json","ROOT_ACTUAL_INPUT_REVIEW_AND_ONE_CALL_RELEASE_v01.json",
      "ROOT_AUTHORIZED_FIRST_CALL_LOCK_v01.json","Invoke-RootReviewedFirstOnce.ps1",
      "api_response.raw.json","request_body.tmp","response_headers.txt","request_manifest.json"]
    assert not [n for n in forbidden if (run/n).exists()]
    val={
     "id":en["id"],"recorded_utc":datetime.now(timezone.utc).isoformat(),"PREPONLY":True,
     "status":"prepared_preview_verified_not_submitted",
     "request":ev(run/"API_PREPARED_REQUEST.json"),"lock":ev(run/"REQUEST_LOCK.json"),
     "preview_proof":ev(run/"API_PREVIEW_PROOF_PREPONLY.json"),
     "guard_refusal_proof":ev(run/"PREVIEW_GUARD_REFUSAL_PROOF.json"),
     "preview_only_runner":ev(run/"Preview-PreparedFirstOnly.ps1"),
     "prompt_and_ordered_reference_hashes_match":True,"all_five_final_inputs_actually_viewed":True,
     "unchanged_rectangle_derivations_reproduced":True,"JOB_and_REGISTRATION_PLAN_hashes_match_initial":True,
     "no_attempt_result_or_root_release_artifacts":True,"no_dispatch_branch_in_own_guard":True,
     "network_absence_basis":"Executed immutable provider's Preview branch, which returns before credential loader, attempt files and network subprocess. This is not an API entitlement/balance test.",
     "configured_model":"gpt-image-2.5-sunburst","quality":"high","n":1,
     "reference_count":5,"size":q["Size"],"background":"transparent",
     "api_calls":0,"native_calls":0,"network_calls":0,"submitted":False,
     "art_review_passed":False,"photography_review_passed":False,"dynamic_validated":False,
     "hidden_geometry_validated":False,"user_accepted":False,
     "central_write_scope":"Own new PREP dirs and task evidence only; no central registry/JOB selection/ROOT_PRIMARY/binding write.",
    }
    vp=run/"API_PREVIEW_VALIDATION_PREPONLY.json";save(vp,val)
    out.append({**en,"preview":ev(run/"API_PREVIEW_PROOF_PREPONLY.json"),"validation":ev(vp),"reference_records":l["references"]})
handoff={
 "schema":"magic-maid.future-two-independent-first-preparation-handoff/1",
 "created_utc":datetime.now(timezone.utc).isoformat(),"status":"PREPONLY_ready_for_root_actual_review_not_released",
 "ids":["ART-G06-01","ART-G07-03"],"entries":out,
 "selection_reason":"Earliest genuine pending ordinary-character groups outside first-dance, no selected asset or own actual return/unknown dispatch; independently prepared G06 and G07.",
 "canonical_source_frames":[476,507],"first_source_nominations":[425,507],
 "source_pts":[254128,270672],"time_base":"1/16000",
 "source_authority":"Original own action/expression/costume/crop; bareheaded loose-gray-sleeve inverted character. Source disc-occluded torso is not visible art.",
 "prop_handling":"Disc surface/rim/ghosts/lyrics remain postproduction layers; actual foreground palm/forearm retained; hidden torso/jaw/mouth not hallucinated.",
 "laterality_and_gravity":"Same anatomical LEFT low ear/nape under actual inverted head roll; roughly viewerLEFT here, not an all-view screen-side rule. No body rotation or mirror. Hair falls downscreen subject to real occlusion; no fixed length/turn count.",
 "input_design":"Five relevant images each; no full maidcap11 head input. G07 old eye-ring context preserved but excluded from formal input, using new unchanged eye-free bob rectangle.",
 "actual_view_evidence_index":ev(TASK/"FINAL_PREPARED_INDEX.json"),
 "old_hard_six_release_helper_not_invoked":True,"root_future_helper_count_change_required":True,
 "future_root_review_and_separate_release_required":True,
 "can_prepare_independently":True,"parallel_submission_not_authorized_here":True,
 "api_calls":0,"native_calls":0,"network_calls":0,"submitted":False,
 "central_registry_JOB_selection_binding_modified":False,
 "art_static_pass":False,"photography_pass":False,"dynamic_pass":False,"user_acceptance":False,
 "skill_read":"C:/Users/11515/.agents/skills/openai-api/SKILL.md",
}
hp=TASK/"PREP_COMPLETE_HANDOFF.json";save(hp,handoff)
md="""# 首段外两项 FIRST：仅准备，未提交

ART-G06-01 与 ART-G07-03 已完成独立源核查、五参考、完整LEFT前缀prompt、high/n1/透明PNG配置和哈希锁。API/native/network均0；未改中央、JOB、ROOT_PRIMARY或绑定；没有返图或艺术通过。

| 状态 | 母帧 / PTS | 最早源提名 | 请求尺寸 |
|---|---|---|---|
| ART-G06-01 | F476 / 254128 | F425 / 226896 | 640×1040 |
| ART-G07-03 | F507 / 270672 | F507 / 270672 | 1344×1024 |

time_base 1/16000。源提名不等于绑定，也不证明全部重复曝光已实际看完；实际看图路径/SHA见各SOURCE_VISIBLE_SCOPE_AUDIT和FINAL_PREPARED_INDEX。

两项都保原倒悬裸头、松灰袖及实际可见边界；476保两裸足，507不加画外腿鞋。盘/盘沿/幽灵/字交后期；盘挡胸腹/口颌不补，盘前掌臂仍保。解剖LEFT按倒悬头轴投影与重力，不翻身/镜像求侧别。

正式输入各五张：原完整guide、此前倒悬裸bob上下文、用户正确11卷-only、pureGRAY、当前源眼口/盘沿裁图。507旧邻稿的灰月牙眼被排除，改无眼hair-only矩形；原试选图保留。正确11完整maidcap头及带光detail不作本镜输入，避免服装/材质竞争。旧邻稿不是当前材料艺术通过。

两份Preview实际均返回 gpt-image-2.5-sunburst / high / n1 / transparent / input_count5 / submitted=false；无mask。仅Preview脚本省略-Preview会在wrapper前拒绝，无发送分支。图像派生可复现，prompt/reference/JOB/REGISTRATION_PLAN均核对锁SHA。

根代理仍需实际查看完整prompt与五个正式输入，再另行锁定release。现有旧FIRST release helper硬编码六图，本任务未调用；不能为了旧helper添加无关第六图。独立镜头组可分别准备，未来实际提交由root按当前授权与并发上限调度。摄影、隐藏几何、播放/动态和用户验收均未认证。

使用技能：[openai-api](C:/Users/11515/.agents/skills/openai-api/SKILL.md)，仅依其Preview流程检查本地参数。
"""
mp=TASK/"PREP_COMPLETE_HANDOFF.md";assert not mp.exists();mp.write_text(md,encoding="utf-8")
print(json.dumps({"handoff":ev(hp),"markdown":ev(mp),"entries":[{"id":x["id"],"run":x["run"],"request":x["request"],"lock":x["lock"],"prompt":x["prompt"],"preview":x["preview"],"validation":x["validation"]} for x in out],"api_calls":0,"network_calls":0},ensure_ascii=False,indent=2))

