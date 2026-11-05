G33-41眼部仅蒙版/spec准备，未应用配色。

两眼实际均normal_open；left iris允许287像素/glint+AA保护13像素，right允许374/保护14。完整640×1056 L二值mask、原尺寸和8x眼部、带坐标图及10x叠图已保。叠图magenta为允许RGB区域，cyan为原小白高光+AA保护；另cyan圆弧图仅几何轮廓，不是修后颜色。

上黑眼线与iris接壤处保存，侧/底旧iris圈纳入本源逐行范围；眼白/皮肤与外缘混色保守保留，修后仍需fresh看是否留下独立黑圈。每眼下浅灰帽按自身宽高/头斜轴配置，过渡1.5原生px。

Root必须亲看FULL_IRIS_MASK_REVIEW_10x与source坐标图后再应用，之后另一Sol独立审实际输出。只读EyeLocalPolicy前置检查通过；当前不授眼修通过、不改中央、不执行颜色/AI。SHA见spec和PREP_ONLY_RECEIPT。
