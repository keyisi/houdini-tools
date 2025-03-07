import hou
import os
import re

def clean_node_name(name):

    # 移除文件扩展名
    name = os.path.splitext(name)[0]
    # 替换无效字符为下划线
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return name

def import_abc_batch():
    # 弹出文件选择对话框，支持多选
    file_paths = hou.ui.selectFile(
        title="选择Alembic文件",
        pattern="*.abc",
        default_value=hou.expandString("$HIP/"),
        multiple_select=True,  # 启用多选
        file_type=hou.fileType.Any  # 允许选择文件
    )

    # 如果没有选择文件，直接返回
    if not file_paths:
        return

    # 将文件路径拆分为元组
    file_paths_list = [path.strip() for path in file_paths.split(';') if path.strip()]

    for node in file_paths_list:
        #print(node)
        # 获取文件名并清理
        nodename = os.path.basename(node)
        nodename = clean_node_name(nodename)

        # 创建 geo 节点
        try:
            geo = hou.node('/obj').createNode('geo', nodename)
            geo.moveToGoodPosition()
            # 创建 alembic 节点
            alc = geo.createNode('alembic')
            alc.parm('fileName').set(node)
            alc.parm('curveFilter').set(0)
            #print(f"成功导入: {nodename}")
        except hou.OperationFailed as e:
            hou.ui.displayMessage(f"创建节点失败: {nodename} - {e}")

import_abc_batch()