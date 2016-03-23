flask pypi proxy
---
- pypi的代理服务器, 用于网速较慢的环境

- 使用自定义服务器安装package($IP换成server ip)
    
    - pip中指定url安装

    ```
    pip install -i http://$IP:9000/simple ipython
    ```

    - 修改默认安装地址参考资料: <http://doc.devpi.net/latest/quickstart-pypimirror.html#permanent-index-configuration-for-pip>

    ```
    # vim $HOME/.pip/pip.conf
    
    [global]
    index-url = http://$IP:9000/simple/
    trusted-host = $IP
    ```


- eggs是一个空目录

- 安装步骤

    - 创建目录

        ```
        sudo mkdir -p /data/web
        sudo chown -R www-data:www-data /data/web
        ```

    - clone

        ```
        cd /data/web
        sudo -u www-data git clone https://github.com/wasw100/flask-pypi-proxy.git
        ```

    - 安装supervisor, 复制 supervisor/flask-pypi-proxy.conf 到supervisor配置目录

    - 安装virtualenv(virtualenvwrapper), 创建虚拟环境flask-pypi-proxy
