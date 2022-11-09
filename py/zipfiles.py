
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @ Date    : 2022/11/6 20:06
# @ Author  : paperClub
# @ Email   : paperclub@163.com
# @ Site    :


import os
import zipfile
import asyncio


async def get_zipfiles(save_zip_path: str,
                file_names:List
              ):
    """ 文件压缩 *zip文件 """

    with zipfile.ZipFile(save_zip_path, "w") as zip:
        for file in file_names:
            zip.write(file, os.path.basename(file))
            os.remove(file)

    return save_zip_path




savefile = "paperclub.zip"
file_names = ["./pdf1.pdf", "./pdf2.pdf"]
loop = asyncio.get_event_loop()
loop.run_until_complete(get_zipfiles(savefile, file_names))
loop.close()