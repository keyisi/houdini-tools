import os
import hou

try:
    # 选择 Alembic 文件
    node = hou.ui.selectFile(title='Select a alembic file', file_type=hou.fileType.Alembic)
    nodename = os.path.basename(node)
    nodename = os.path.splitext(os.path.basename(node))[0]
    #print(nodename)
    # 检查用户是否取消了选择
    if node is None:
        pass  # 退出脚本
        
    # 创建 Alembic Archive 节点
    geo = hou.node('/obj').createNode('alembicarchive',nodename)
    geo.parm('fileName').set(node)
    geo.parm('buildSubnet').set(0)
    geo.parm('channelRef').set(1)
    geo.parm('buildHierarchy').pressButton()
    
        # 在节点内部查找 camera 节点
    def find_camera_node(node):
        for child in node.children():
            if child.type().name() == 'cam':
                return child
            # 递归查找子节点的子节点
            found_camera = find_camera_node(child)
            if found_camera:
                return found_camera
        return None
    
    # 查找 camera 节点
    camera_node = find_camera_node(geo)
    
    if camera_node:
        inputs = hou.ui.readMultiInput(
        message="Enter resolution:",
        input_labels=("Width (X):", "Height (Y):"),
        buttons=("OK", "Cancel"),
        initial_contents=("1920", "1080")  # 默认值
    )
    
    
        # 检查用户是否取消了输入
        if inputs[0] == 1:  # 1 表示用户点击了 "Cancel"
            print("Resolution input was canceled.")
            exit()
               
        resx_str, resy_str = inputs[1]
        myresx = int(resx_str)  # 将输入的宽度转换为整数
        myresy = int(resy_str)  # 将输入的高度转换为整数
      
        camera_node.parm('resx').set(myresx)  # 设置水平分辨率
        camera_node.parm('resy').set(myresy)  # 设置垂直分辨率

        #print(f"Found camera node: {camera_node.path()}")
    else:
        geo.destroy()
        hou.ui.displayMessage("当前文件未找到相机")
        

except:
    pass