# 导入模块
import os
import glob
import pyJianYingDraft as draft
from pyJianYingDraft import Intro_type, Transition_type, trange
from pyJianYingDraft import Draft
import pandas as pd
from datetime import datetime
import re
import random
from pyJianYingDraft import Clip_settings
from pyJianYingDraft.metadata.video_effect_meta import Video_scene_effect_type
from pyJianYingDraft import Keyframe_property, SEC
import time
from pyJianYingDraft import Mask_type
import copy

tutorial_asset_dir = os.path.join(os.path.dirname(__file__), 'readme_assets', 'tutorial')

# 定义片头视频文件夹路径
HeadVideoFolder_path = 'E:\\Resources\\自媒体\\二创\\素材'
# 定义背景音乐文件夹路径
BgAudioFolder_path = 'E:\\Resources\\测试\\背景音乐'


# 获取文件夹中所有视频文件的路径
video_files = glob.glob(os.path.join(HeadVideoFolder_path, '*.mp4'))
allAudioFolder= glob.glob(os.path.join(BgAudioFolder_path, '*.mp3')) + glob.glob(os.path.join(BgAudioFolder_path, '*.wav')) + glob.glob(os.path.join(BgAudioFolder_path, '*.flac'))


# 获取当前的年、月、日
now = datetime.now()


DraftIndex=0

# 创建一个空列表
my_list = []

draft_folder = draft.Draft_folder("D:\\Software\\JianYin\\JianyingPro Drafts")
script1 = draft_folder.load_template("9月14日")
script1.inspect_material()

#  Resource id: 7243239177112931588 '竹叶飘落'    
#         Resource id: 7209913590357167415 '柳叶'        
#         Resource id: 7243239177112931588 '竹叶飘落'    
#         Resource id: 7243240495667793185 '茱萸果子树叶'
#         Resource id: 7209913590357167415 '柳叶'        
#         Resource id: 7243240495667793185 '茱萸果子树叶'
# Resource id: 7470436285652684056 '玫瑰'
#         Resource id: 7472653192984284441 '芭比粉妇女节女神节蝴蝶装饰'

# 遍历视频文件
for i in range(len(video_files)):#for file in video_files:


    #项目名
    DraftName= f"{now.year}_{now.month}_{now.day}_{DraftIndex}"
    DraftIndex+=1
    file = video_files[i]

    # 新建项目
    New = Draft.Draft(DraftName)
    New.save()

    Head_video_material = draft.Video_material(os.path.join(HeadVideoFolder_path, os.path.basename(file)))  #按顺序获取片头视频
    Bg_audio_material = draft.Audio_material(os.path.join(BgAudioFolder_path, os.path.basename(random.choice(allAudioFolder)))) #随机获取背景音乐
    
    # 创建剪映草稿
    script = draft.Script_file(Head_video_material.width, Head_video_material.height) # 1080x1080分辨率

    # 添加音频、视频和文本轨道
    script.add_track(draft.Track_type.video,track_name="主画面",absolute_index=0)
     # 添加音频、视频和文本轨道
    script.add_track(draft.Track_type.video,track_name="画中画",absolute_index=1)
    script.add_track(draft.Track_type.sticker,track_name="贴纸",absolute_index=2)
    script.add_track(draft.Track_type.sticker,track_name="贴纸1",absolute_index=3)

    script.add_track(draft.Track_type.audio)

    # script.add_track(draft.Track_type.sticker,track_name="贴纸2",absolute_index=4)
    # script.add_track(draft.Track_type.sticker,track_name="贴纸3",absolute_index=5)
    # script.add_track(draft.Track_type.sticker,track_name="贴纸4",absolute_index=6)
    # script.add_track(draft.Track_type.sticker,track_name="贴纸5",absolute_index=7)
    
    script.add_material(Head_video_material).add_material(Head_video_material).add_material(Bg_audio_material)#.add_material(sticker_material) # 随手添加素材是好习惯

    # 创建视频片段
    video_segment = draft.Video_segment(Head_video_material,draft.Timerange(0, Head_video_material.duration) )# 片段将位于轨道上的0s-4.2s（取素材前4.2s内容，注意此处4.2s表示持续时长）

# 创建画中画视频片段
    video_segment2 = draft.Video_segment(Head_video_material,trange(Head_video_material.duration-3000000, "2.7s") ,source_timerange=trange(Head_video_material.duration-3000000,"2.7s"),volume=0,speed=0.9)

# #0.9倍速
#     video_segment = draft.Video_segment(Head_video_material2,draft.Timerange(0, Head_video_material2.duration),speed=0.9)

    video_segment2.add_mask(Mask_type.镜面, center_x=0,center_y=0, rotation=75,size=0.5,feather=10)
    # video_segment2.mask.add_keyframe(Keyframe_property.position_x,-Head_video_material.width,1)
    
    # sticker_segment=draft.Sticker_segment("7243239177112931588",draft.Timerange(0, Head_video_material.duration)).add_keyframe(Keyframe_property.position_x,video_segment.duration,-0.7).add_keyframe(Keyframe_property.position_y,video_segment.duration,0.5).add_keyframe(Keyframe_property.uniform_scale,video_segment.duration,0.6)
    # sticker_segment1=draft.Sticker_segment("7209913590357167415",draft.Timerange(0, Head_video_material.duration)).add_keyframe(Keyframe_property.position_x,video_segment.duration,0.8).add_keyframe(Keyframe_property.position_y,video_segment.duration,0.7).add_keyframe(Keyframe_property.uniform_scale,video_segment.duration,0.6)
    # sticker_segment2=draft.Sticker_segment("7243239177112931588",draft.Timerange(0, Head_video_material.duration)).add_keyframe(Keyframe_property.position_x,video_segment.duration,-0.3).add_keyframe(Keyframe_property.position_y,video_segment.duration,0.5).add_keyframe(Keyframe_property.uniform_scale,video_segment.duration,0.6)
    # sticker_segment3=draft.Sticker_segment("7243240495667793185",draft.Timerange(0, Head_video_material.duration)).add_keyframe(Keyframe_property.position_x,video_segment.duration,-0.5).add_keyframe(Keyframe_property.position_y,video_segment.duration,0.7).add_keyframe(Keyframe_property.uniform_scale,video_segment.duration,0.6)
    # sticker_segment4=draft.Sticker_segment("7209913590357167415",draft.Timerange(0, Head_video_material.duration)).add_keyframe(Keyframe_property.position_x,video_segment.duration,0.3).add_keyframe(Keyframe_property.position_y,video_segment.duration,0.7).add_keyframe(Keyframe_property.uniform_scale,video_segment.duration,0.6)
    # sticker_segment5=draft.Sticker_segment("7243240495667793185",draft.Timerange(0, Head_video_material.duration)).add_keyframe(Keyframe_property.position_x,video_segment.duration,0.4).add_keyframe(Keyframe_property.position_y,video_segment.duration,0.7).add_keyframe(Keyframe_property.uniform_scale,video_segment.duration,0.6)

    sticker_segment=draft.Sticker_segment("7470436285652684056",draft.Timerange(0, Head_video_material.duration)).add_keyframe(Keyframe_property.position_x,video_segment.duration,-0.85).add_keyframe(Keyframe_property.position_y,video_segment.duration,-0.8).add_keyframe(Keyframe_property.rotation,video_segment.duration,318).add_keyframe(Keyframe_property.uniform_scale,video_segment.duration,0.2)
    sticker_segment1=draft.Sticker_segment("7472653192984284441",draft.Timerange(0, Head_video_material.duration)).add_keyframe(Keyframe_property.position_x,video_segment.duration,0.8).add_keyframe(Keyframe_property.position_y,video_segment.duration,0.7).add_keyframe(Keyframe_property.uniform_scale,video_segment.duration,0.5)


    video_segment.add_effect(Video_scene_effect_type.摇晃运镜,[0,10,5,15,15])
    video_segment.add_effect(Video_scene_effect_type.录制边框_III)
    video_segment.add_effect(Video_scene_effect_type.爱心啵啵,[30,50])
    video_segment.add_effect(Video_scene_effect_type.抽帧拖影,[0,0,30,0])
    video_segment.add_effect(Video_scene_effect_type.画质清晰,[0,100,40,0,100,50,30])
    #video_segment.add_effect(Video_scene_effect_type.电光描边,[100,100,50,100,50,50])   #颜色，摇晃强度，电光强度，大小，强度,旋转
    video_segment.add_keyframe(Keyframe_property.saturation, video_segment.duration, 0.7) # 片段结束时0.1饱和度
    video_segment.add_keyframe(Keyframe_property.contrast, video_segment.duration, 0.7) # 片段结束时0.1对比度

    # # 将上述片段添加到轨道中
    script.add_segment(video_segment,"主画面")#.add_segment(sticker_segment)
    script.add_segment(video_segment2,"画中画")
    script.add_segment(sticker_segment,"贴纸")
    script.add_segment(sticker_segment1,"贴纸1")
    # script.add_segment(sticker_segment2,"贴纸2")
    # script.add_segment(sticker_segment3,"贴纸3")
    # script.add_segment(sticker_segment4,"贴纸4")
    # script.add_segment(sticker_segment5,"贴纸5")

    audio_segment = draft.Audio_segment(Bg_audio_material,
                                        trange("0s", min(Bg_audio_material.duration, video_segment.end if video_segment.end>Bg_audio_material.duration else video_segment.end)), # 片段将位于轨道上的0s-5s（注意5s表示持续时长而非结束时间）
                                        volume=0.4)         # 音量设置为60%(-4.4dB)
    audio_segment.add_fade("0.5s", "0s")                      # 增加一个1s的淡入
    script.add_segment(audio_segment)

        #print(f"Text: {textTemp}, Duration: {duration} minutes")bobo

    # 保存草稿（覆盖掉原有的draft_content.json）
    script.dump(f"D:/Software/JianYin/JianyingPro Drafts/{DraftName}/draft_content.json")
    my_list.append(DraftName)

os.startfile(os.path.join(os.path.join(os.environ['USERPROFILE']), 'D:\\Software\\JianYin\\JianyingPro', 'JianyingPro.exe'))
#等待两秒
time.sleep(2)
#此前需要将剪映打开，并位于目录页
ctrl = draft.Jianying_controller()
for file in my_list:
    # 然后即可导出指定名称的草稿
    ctrl.export_draft(file,output_dir=None)  #注意导出结束后视频才会被剪切至指定位置
   

    