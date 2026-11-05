from pathlib import Path
from datetime import datetime, timezone
import json,hashlib
from PIL import Image
P=Path("D:/CODEX/魔术之心")
B=P/"art/full_character_redraw_1080p_v01"
I="ART-G33-64";A=B/"drawings"/I;V=A/"v01"
R=V/"direct_first_api_source2593_ownPose_userThinRibbon_danceB_tls12_v20"
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return Path(p).read_text(encoding="utf-8-sig")
def j(p):return json.loads(read(p))
def rec(p):return {"path":str(Path(p)),"sha256":h(p)}
def write(p,o):Path(p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
assert not R.exists(),"Prep run already exists; do not overwrite."
job=V/"JOB.json";reg=V/"REGISTRATION_PLAN.json";jj=j(job);rr=j(reg)
assert jj["id"]==I and jj["source_frame"]==2593 and jj["source_pts"]==1384320 and jj["source_reuse_scope"] is None and jj["status"]=="pending"
assert jj["output_size"]==[624,1072] and rr["guide_dimensions"]==[624,1072]
src=Path(jj["source_image"]);guide=V/"inputs/source_pose_guide.png"
assert h(src)==jj["source_image_sha256"]=="52aa080f936f1ddc10ff8dddf9d04278e937dce9216c8cf8bec2f7c6a738b4f7"
assert Image.open(guide).size==(624,1072)
progress=B/"PROGRESS.json";registry=B/"ASSET_REGISTRY.json"
pp=j(progress);ar=j(registry);rows=[x for x in pp["records"] if x["id"]==I]
assert len(rows)==1 and rows[0]["status"]=="pending" and not rows[0].get("image") and not ar.get(I,{}).get("image")
allfiles=sorted(x for x in A.rglob("*") if x.is_file())
execution_names={"attempt.json","result.json","BUILTIN_GENERATION.json","api_response.raw.json","request_manifest.json","ROOT_DIRECT_EXECUTION_RELEASE.json"}
assert not any(x.name in execution_names for x in allfiles)
assert not any(x.name in {"character_api_original.png","character_imggen_original.png","character_eye_gray_local.png"} for x in allfiles)
alias=B/"ALIAS_BINDING_HISTORY.jsonl"
assert not alias.exists() or I not in read(alias)
prevrows=[x for x in pp["records"] if x["id"]=="ART-G33-63"]
prev={"id":"ART-G33-63","progress_status":prevrows[0].get("status") if prevrows else None,"registry_status":ar.get("ART-G33-63",{}).get("status"),"image":ar.get("ART-G33-63",{}).get("image"),"not_input":True,"prior_policy_not_certified":True,"root_observation_only":"Old coil had excess turns and narrow cylinder appearance; no fresh visual certification of that old art is made by this PREP."}
defaults=P/"image_defaults.json";d=j(defaults);ep=d["eye_color_policy"]
assert h(ep["path"])==ep["sha256"]
assert j(ep["path"])["policy_id"]=="post_pass_normal_open_eye_dance_B_override_20261104_v04"
assert d["api_request_policy"]["retry"]==1
hp=d.get("source_hairstyle_policy"); hs=j(hp["path"])
entry=hs["states"].get(I,{})
assert entry.get("generation_allowed",True) and entry.get("mode","drill")=="drill"
reqpolicy=B/"GOAL_CURL_ASSESSMENT_REQUIREMENTS_20261104_v10.json";c=j(reqpolicy)
assert c["construction_policy_id"]=="hollow_two_large_one_small_20261102_v04"
provider=P/"scripts/Invoke-ReferenceImage-Tls12Recovery20261104.ps1"
assert h(provider)=="664a12030846fed90a6347248587fc0b4ffa104ab9a0b53a33ffa573fe99c866"
bproof=B/"review/USER_DANCE_B_LOW_SATURATION_EYES_20261104_v04/USER_EYE_STYLE_ACCEPTANCE.json"
bf=j(bproof)["color_fields"][0]["image"]
assert h(bf["path"])==bf["sha256"]=="02d75215432eb8fd0ef515655804056d911166faff51e3c2ad32cc663d20391a"
thin=B/"inputs/reviewed_thin_first_band_no_eyes_20261104_v01/THIN_FIRST_BAND_ONLY_NO_EYES.png"
thinproof=thin.parent/"PROVENANCE.json"
assert h(thin)==j(thinproof)["output"]["sha256"]=="514217b3596451213507ff0b93f5df9ae82495641e0da4b988a3f6254247fc3d"
refs=[
 (guide,"own exact F2593 full pose, line style, facial action, clothing, both feet and visibility authority"),
 (B/"inputs/graybob_identity_WITHOUT_EYES_20261104_v01/BOB_BANGS_COLOR_NO_EYES.png","flat gray bob/bangs material and identity only; no eyes or pose"),
 (B/"drawings/ART-G13-28/v01/direct_first_api_source1313_fullApprovedCoil_lowEarNape_postPassEye_v12/inputs/ref3_USER_APPROVED_X01_COMPLETE_UPPER_SMALL_RETURN_C_READONLY_v02.png","complete continuous 2Large + trueSmall then C construction only; not incidental bead location, axis, costume or other action"),
 (Path(bf["path"]),"user selected dance B interior low-saturation two-gray field and soft lower cap only; no eye shape, glint, pose or centered dark blemish"),
 (thin,"first large turn front ribbon thickness ONLY, crop excludes complete coil; not turn-count or diameter/pose/root placement authority")
]
assert h(refs[1][0])=="85645183cf8ec82990857aa8789e4ae42959ebbba4688fe392f37e55ce03ed1f"
assert h(refs[2][0])=="8e0d9a8682331a2dc7684f05becdead3ec47e699540bd83a45a83810b6464b10"
R.mkdir(parents=True,exist_ok=False)
prompt=R/"prompt_api.txt"
action="自身F2593近正面、两眼正常睁开但各自眼形/眼位和小glint保持，闭口小弧笑。画左臂外抬屈肘、宽白袖口，手一根指斜上伸，其余指保原简笔弯折与指缝；画右肘垂下、低位白袖口、裸掌张开，指尖向外和向下分开。双手姿势不同，不能复制。黑长袖黑长裙、红胸结金扣、白帽褶+两黑叶、白肩褶、长白围裙和原右侧后带。左侧鞋较低略斜，右侧鞋较高内收；两条裸小腿、踝带和两只完整黑鞋都保源错位，不补隐藏腿也不裁脚。"
text="""绘制一张 F2593 原PV的透明人物层，624×1072。以图1自身原片为动作、五官、比例、衣装、笔触及可见范围的唯一依据。原粉底和白字留后期，画面只保人物；按图1原轮廓留足帽顶、两侧手指和两个鞋尖，不放大挤出边框。

"""+action+"""

头发换灰短bob，图2只供bob与简笔颜色。保图1近正面头颌与颈肩，不镜像。人物解剖LEFT的根位在画右自身低耳后／bob下缘／颈后，恰好两颗红珠先接同一发束，再贴画右本肩的白肩褶与领胸前自然重叠。不要高侧脑接茎、肩外悬挂、另起第二束，亦不搬参考图珠位或头角。

图3只供完整发带构造。正常体量的单条连续宽灰发带沿空心轴翻回：第一大转的灰正面与不透明灰返回、第二大转的灰正面与不透明返回、一个独立真实较小的灰正面与返回，最后才连成渐细C钩。小卷不是尾钩内的洞，不要让第二大转直接变C、也不把小卷画成第三个同大的主圈。灰返回实体保留，真实露空见到后方衣物或透明底；有原肩/手遮挡则顺势遮挡，不为了固定孔数挖灰或补隐藏段。薄荷只作简笔材质边，灰为主体；不画银白亮带、金属渐变或密集发丝。

图5仅参考首大转正面发带较薄的弧带画法，保持两大转的正常卷径和头肩体量，不能缩成小挂件、蓬大垂腰或照搬图5的珠、肩褶、方向、开口与其它圈。图5的片段不用于计圈；完整顺序以图3为准。

图4仅采用用户所选B低饱和深灰与较柔低反差的底部浅灰上凸圆弧，适配每只自身眼轴；不描摹其暗斑、黑中心、外虹膜、眼白、睫线、高光或眼形。不添独立黑瞳点、眼下装饰点或痣；保原真的下睫笔道、鼻点、原小白高光与开合。原手书墨线与简笔平涂保留，不向量重画或统一精修。返图人物先实际通过主评与独审，正常开眼才另行局部Python眼内B色校准，本请求不以首绘颜色免除后审。
"""
prompt.write_text(text,encoding="utf-8")
q={
"schema":"direct_missing_first_own_pose_user_thin_ribbon_dance_B_tls12_v20",
"id":I,"source_frame":2593,"source_pts":1384320,"source_time_base":"1/16000","source":rec(src),"guide":rec(guide),"guide_frame":2593,"guide_pts":1384320,
"parameters":{"PromptFile":str(prompt),"InputImages":[str(p) for p,_ in refs],"OutputDirectory":str(R),"Size":"624x1072","Quality":"high","Background":"transparent","OutputFileName":"character_api_original.png","Stage":"ART-G33-64_MISSING_FIRST_OWN2593_THIN_RIBBON_B_TLS12_V20","DrawingId":I,"HairstyleMode":"drill","OperationKind":"first_missing"},
"model":"gpt-image-2.5-sunburst","n":1,"retry":1,"provider":rec(provider),"prompt":rec(prompt),"refs":[rec(p) for p,_ in refs],
"eye_color_policy":ep,"requirements":rec(reqpolicy),"curl_structure_policy_id":c["construction_policy_id"],
"reference_roles":[{"index":i,"path":str(p),"scope":role} for i,(p,role) in enumerate(refs,1)],
"own_action":action,
"thin_first_band_provenance":rec(thinproof),"B_field_acceptance_provenance":rec(bproof),
"source_provenance":{"JOB":rec(job),"registration":rec(reg),"source_bbox":jj["source_bbox_xyxy"],"crop":jj["crop_xyxy"],"source_to_guide_transform":rr,"guide_is_reference_only_not_photography_proof":True},
"previous_family_history_only":prev,
"first_inventory":{"job_status":jj["status"],"progress_path":str(progress),"progress_row":rows[0],"registry_path":str(registry),"existing_selected_or_aliased_image":False,"alias_history_contains_id":False,"all_prior_nested_files":[str(x.relative_to(A)) for x in allfiles],"prior_attempt_result_builtin_or_return_found":False,"source_reuse_scope":None},
"actual_prep_viewed":[rec(p) for p in [src]+[p for p,_ in refs]],
"root_release_required":True,"root_release_granted":False,"prep_only":True,"submitted":False,"API_calls":0,
"execution_boundary":"ROOT actual review of exact inputs/prompt and distinct one-logical-request release required. Direct validated TLS12 wrapper only. Existing Invoke-ReviewedMissingFirst.ps1 hardcodes the non-TLS wrapper and cannot be used as-is for this TLS release. Do not substitute provider or retry an unknown result.",
"prepared_utc":datetime.now(timezone.utc).isoformat()
}
p=R/"DIRECT_REQUEST.json";write(p,q)
write(R/"REQUEST_LOCK.json",{"id":I,"request":rec(p),"prompt":q["prompt"],"provider":q["provider"],"refs":q["refs"],"source":q["source"],"guide":q["guide"],"eye_color_policy":ep,"root_release_granted":False,"submitted":False,"API_calls":0})
print(json.dumps({"run":str(R),"request":rec(p),"prompt":rec(prompt),"lock":rec(R/"REQUEST_LOCK.json"),"source":q["source"],"guide":q["guide"],"previous_history":prev,"first_inventory":q["first_inventory"]},ensure_ascii=False))

