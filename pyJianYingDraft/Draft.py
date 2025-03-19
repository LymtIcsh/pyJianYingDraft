import os
import time
from pyJianYingDraft import util,template,material,track

class Draft:

    drafts_folder = "D:\Software\JianYin\JianyingPro Drafts"
    template_folder = "./template json/"
    content_file = "draft_content.json"
    meta_info_file = "draft_meta_info.json"

    def __init__(self, name:str="Test"):
        # 路径变量
        self.name = name
        self.folder = os.path.join(self.drafts_folder, name)
        self.content_path = os.path.join(self.folder, self.content_file)
        self.meta_info_path = os.path.join(self.folder, self.meta_info_file)
        # 新建项目文件夹
        util.new_folder(self.folder)
        # 读取草稿模板
        self.content = util.read_json(os.path.join(self.template_folder,self.content_file))
        self.meta_info = util.read_json(os.path.join(self.template_folder,self.meta_info_file))
        # 初始化草稿内容信息
        self.content['id'] = util.generate_id()
        # 初始化素材信息
        self.meta_info['id'] = util.generate_id()
        self.meta_info['draft_fold_path'] = self.folder.replace("\\",'/')
        self.meta_info['draft_timeline_metetyperials_size_'] = 0
        self.meta_info['tm_draft_create'] = time.time()
        self.meta_info['tm_draft_modified'] = time.time()
        self.meta_info['draft_root_path'] = self.drafts_folder.replace("/","\\")
        self.meta_info['draft_removable_storage_device'] = self.drafts_folder.split(':/')[0]
        ## 创建变量
        # self.draft_materials:list = self.meta_info['draft_materials'][0]['value'] # 草稿素材库
        # self.content_materials:list = self.content['materials'] # 内容素材库
        # self.tracks = track.Tracks() # 轨道
        self.materials = {}

    def _medai_tpye(self,media):
        if type(media) == str:
            # 当media为文件路径时
            if os.path.exists(media):
                return 'path'
            else:
                # 文件不存在
                return 'text'
        else:
            return media

    
    def save(self):
        """保存草稿"""
       # self.content['tracks'] = self.tracks._composite() # 覆盖轨道
        util.write_json(self.content_path,self.content)
        util.write_json(self.meta_info_path,self.meta_info)

# if __name__ == "__main__":
#     # 新建项目
#     draft = Draft("草稿")
#     text = material('Hello World')
#     text.change_color('#ABCABC')
#     draft.add_media_to_track(text,duration=3000000)
#     draft.save()