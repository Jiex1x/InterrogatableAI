# Alternative Deployment Options

由于Railway的4GB镜像限制，当前项目（包含torch等大型依赖）可能无法部署。

## 推荐方案

### 方案1: Render (推荐)
- **镜像限制**: 无明确限制（更宽松）
- **免费额度**: 750小时/月
- **优点**: 对大型依赖更友好
- **步骤**: 类似Railway，使用Procfile

### 方案2: Streamlit Cloud (最简单)
- **限制**: 1GB文件大小限制
- **优点**: 专为Streamlit设计，最简单
- **缺点**: PDF文件可能太大
- **步骤**:
  1. 访问 https://share.streamlit.io
  2. 连接GitHub仓库
  3. 设置环境变量
  4. 部署

### 方案3: 本地 + ngrok (临时演示)
- **优点**: 无限制，最快
- **缺点**: 需要本地运行
- **步骤**:
  ```bash
  # 终端1: 运行应用
  streamlit run app.py
  
  # 终端2: 运行ngrok
  ngrok http 8501
  ```

### 方案4: 优化项目（减少依赖）
可以考虑：
- 使用更轻量的embedding模型
- 移除不必要的依赖
- 使用API服务替代本地模型

## 当前问题

镜像大小10GB > Railway限制4GB

主要原因：
- torch (~2-3GB)
- transformers (~1GB)
- sentence-transformers模型下载
- 其他依赖

## 建议

**最快方案**: 使用Render部署
1. 注册 https://render.com
2. 创建Web Service
3. 使用相同的Procfile和requirements.txt
4. Render对大型依赖更宽容

