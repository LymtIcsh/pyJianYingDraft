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

tutorial_asset_dir = os.path.join(os.path.dirname(__file__), 'readme_assets', 'tutorial')

# 定义片头视频文件夹路径
HeadVideoFolder_path = 'E:\\Resources\\测试\\片头'
HeadVideoFolder_path1 = 'E:\\Resources\\测试\\视频1'
HeadVideoFolder_path2 = 'E:\\Resources\\测试\\视频2'
HeadVideoFolder_path3 = 'E:\\Resources\\测试\\视频3'
HeadVideoFolder_path4 = 'E:\\Resources\\测试\\视频4'
valueText = "那年18岁\n边上学便做电商\n爽了..."
# 定义背景音乐文件夹路径
BgAudioFolder_path = 'E:\\Resources\\测试\\背景音乐'

# 获取文件夹中所有视频文件的路径
video_files = glob.glob(os.path.join(HeadVideoFolder_path, '*.mp4'))
video_files1 = glob.glob(os.path.join(HeadVideoFolder_path1, '*.mp4'))
video_files2 = glob.glob(os.path.join(HeadVideoFolder_path2, '*.mp4'))
video_files3 = glob.glob(os.path.join(HeadVideoFolder_path3, '*.mp4'))
video_files4 = glob.glob(os.path.join(HeadVideoFolder_path4, '*.mp4'))
allAudioFolder= glob.glob(os.path.join(BgAudioFolder_path, '*.mp3')) + glob.glob(os.path.join(BgAudioFolder_path, '*.wav')) + glob.glob(os.path.join(BgAudioFolder_path, '*.flac'))

# 获取当前的年、月、日
now = datetime.now()


DraftIndex=0

# 创建一个空列表
my_list = []

# 遍历视频文件
for i in range(len(video_files)):#for file in video_files:


    #项目名
    DraftName= f"{now.year}_{now.month}_{now.day}_{DraftIndex}"
    DraftIndex+=1
    file = video_files[i]
    file1 = video_files1[i]
    file2 = video_files2[i]
    file3 = video_files3[i]
    file4 = video_files4[i]

    # 新建项目
    New = Draft.Draft(DraftName)
    New.save()

    # 创建剪映草稿
    script = draft.Script_file(1080, 1920) # 1080x1080分辨率

    # 添加音频、视频和文本轨道
    script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)

    # 从本地读取音视频素材和一个gif表情包
    Bg_audio_material = draft.Audio_material(os.path.join(BgAudioFolder_path, os.path.basename(random.choice(allAudioFolder)))) #随机获取背景音乐
    Head_video_material = draft.Video_material(os.path.join(HeadVideoFolder_path, os.path.basename(file)))  #按顺序获取片头视频
    Head_video_material1 = draft.Video_material(os.path.join(HeadVideoFolder_path1, os.path.basename(file1)))  #按顺序获取第二视频
    Head_video_material2 = draft.Video_material(os.path.join(HeadVideoFolder_path2, os.path.basename(file2)))  #按顺序获取第三视频
    Head_video_material3 = draft.Video_material(os.path.join(HeadVideoFolder_path3, os.path.basename(file3)))  #按顺序获取第二视频
    Head_video_material4 = draft.Video_material(os.path.join(HeadVideoFolder_path4, os.path.basename(file4)))  #按顺序获取第三视频
  #  sticker_material = draft.Video_material(os.path.join(tutorial_asset_dir, 'sticker.gif'))
    script.add_material(Bg_audio_material).add_material(Head_video_material).add_material(Head_video_material1).add_material(Head_video_material2).add_material(Head_video_material3).add_material(Head_video_material4)#.add_material(sticker_material) # 随手添加素材是好习惯

    # # 创建音频片段
    # audio_segment = draft.Audio_segment(Bg_audio_material,
    #                                     trange("0s", min(0, Bg_audio_material.duration)), # 片段将位于轨道上的0s-5s（注意5s表示持续时长而非结束时间）
    #                                     volume=0.8)         # 音量设置为60%(-4.4dB)
    # audio_segment.add_fade("0.5s", "0s")                      # 增加一个1s的淡入

    # 创建视频片段
    video_segment = draft.Video_segment(Head_video_material, trange("0s","3s" if Head_video_material.duration>3000000 else Head_video_material.duration),volume=0) # 片段将位于轨道上的0s-4.2s（取素材前4.2s内容，注意此处4.2s表示持续时长）
    #video_segment.add_animation(Intro_type.交错开幕)                              # 添加一个入场动画“斜切”

        # 创建第二个视频片段
    video_segment1 = draft.Video_segment(Head_video_material1, trange(video_segment.end, "3s" if Head_video_material1.duration>3000000 else Head_video_material1.duration),volume=0) # 紧跟上一片段，长度与gif一致
    video_segment1.add_animation(Intro_type.渐显)

    # 创建第三个视频片段
    video_segment2 = draft.Video_segment(Head_video_material2, trange(video_segment1.end, "3s" if Head_video_material2.duration>3000000 else Head_video_material2.duration),volume=0) # 紧跟上一片段，长度与gif一致

      # 创建第三个视频片段
    video_segment3 = draft.Video_segment(Head_video_material3, trange(video_segment2.end, "3s" if Head_video_material3.duration>3000000 else Head_video_material3.duration),volume=0) # 紧跟上一片段，长度与gif一致

 

      # 创建第三个视频片段
    video_segment4 = draft.Video_segment(Head_video_material4, trange(video_segment3.end, "3s" if Head_video_material4.duration>3000000 else Head_video_material4.duration),volume=0) # 紧跟上一片段，长度与gif一致


    # sticker_segment = draft.Video_segment(sticker_material,
    #                                     trange(video_segment4.end, sticker_material.duration)) # 紧跟上一片段，长度与gif一致
    
    # # 为二者添加一个转场
    # video_segment4.add_transition(Transition_type.信号故障) # 注意转场添加在“前一个”视频片段上

    # 创建音频片段
    audio_segment = draft.Audio_segment(Bg_audio_material,
                                        trange("0s", min(Bg_audio_material.duration, video_segment4.end if video_segment4.end>Bg_audio_material.duration else video_segment4.end)), # 片段将位于轨道上的0s-5s（注意5s表示持续时长而非结束时间）
                                        volume=0.8)         # 音量设置为60%(-4.4dB)
    audio_segment.add_fade("0.5s", "0s")                      # 增加一个1s的淡入


    # 将上述片段添加到轨道中
    script.add_segment(audio_segment).add_segment(video_segment).add_segment(video_segment1).add_segment(video_segment2).add_segment(video_segment3).add_segment(video_segment4)#.add_segment(sticker_segment)

  


    # 使用正则表达式按中文标点符号分割 还有空格
    sentences = re.split(r'[，。！？； ]', valueText)

    # 移除空字符串
    sentences = [sentence for sentence in sentences if sentence]

    uptext_segment=0
    for textTemp in sentences:

    # 计算文本的语速时间长度
    # 假设语速是每分钟150个单词
        word_count = len(textTemp.split())
        speed =0.000002  # 单位：单词/分钟
        duration = word_count / speed  # 单位：分钟
        # 创建一行类似字幕的文本片段并添加到轨道中
        text_segment = draft.Text_segment(textTemp, trange(uptext_segment, duration*2),  # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                        style=draft.Text_style(color=(1.0, 1.0, 0.0),size=12,align=1),                # 设置字体颜色为黄色
                                        clip_settings=draft.Clip_settings(transform_y=-0.8))          # 模拟字幕的位置
        script.add_segment(text_segment)
        uptext_segment=text_segment.end
        #print(f"Text: {textTemp}, Duration: {duration} minutes")

    # 保存草稿（覆盖掉原有的draft_content.json）
    script.dump(f"D:/Software/JianYin/JianyingPro Drafts/{DraftName}/draft_content.json")
    my_list.append(DraftName)

# 此前需要将剪映打开，并位于目录页
ctrl = draft.Jianying_controller()
for file in my_list:
    # 然后即可导出指定名称的草稿
    ctrl.export_draft(file,output_dir=None)  #注意导出结束后视频才会被剪切至指定位置
   

    