# ImagineAI - Image Generation Chatbot 🎨

ImagineAI is a highly polished, interactive Image Generation Chatbot built using Python and Streamlit. It allows users to write prompts, apply artistic style presets, customize dimensions and generation seeds, and view/download the generated images.

The app supports multiple providers, including **Pollinations.ai** (which requires zero setup/keys!), **Hugging Face Hub** (FLUX.1-schnell model), and **OpenAI DALL-E**.

---

## ✨ Features

- **Rich, Premium Interface:** Modern, responsive UI utilizing custom glassmorphic cards, typography from Google Fonts, gradients, hover animations, and dark/light compatibility.
- **Style-Conditioned Prompts:** Overlay presets like *Cyberpunk*, *Anime*, *Photorealistic*, *3D Render/Pixar*, *Origami*, *Surrealism*, and more.
- **Multi-API Provider Engine:**
  - **Pollinations.ai** (Free, instant, no key required)
  - **Hugging Face API** (Free serverless Hugging Face tokens)
  - **OpenAI API** (DALL-E 3)
- **Advanced Control Parameters:** Negative prompts, custom aspect ratios/resolutions, generation seed setting for reproducibility, and image count selector (1 to 4 images generated in a grid).
- **Session History & Gallery:** Automatically saves your generation history, shows previous designs in a sidebar-less tab gallery, and allows you to reload any past prompt back into the generator with one click.
- **Surprise Me (Random Prompt Generator):** Instantly suggests creative prompts to spark your imagination.
- **Client-Side Downloads:** Click a button to directly download generated images as PNGs.

---

## 📂 Project Structure

```text
image-generation-chatbot/
├── .env.example          # Environment variables template
├── app.py                # Main Streamlit application entry point
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── src/
    ├── __init__.py
    ├── api.py            # API request handlers (Pollinations, HF, OpenAI)
    ├── prompts.py        # Preset styles & prompt modification helpers
    └── ui.py             # Custom HTML/CSS styling & template rendering
```

---

## 🚀 Running Locally

Follow these steps to run the application on your local machine.

### Prerequisites
Make sure you have **Python 3.8+** installed.

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd image-generation-chatbot
```

### 2. Set up a virtual environment
On Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```
On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application
```bash
streamlit run app.py
```
This will start a local server and automatically open the application in your default browser at `http://localhost:8501`.

---

## 🔑 How to Add Your API Keys

You have three ways to configure your API keys:

### Option A: Local `.env` file (Recommended for Local Dev)
1. Copy the template `.env.example` file and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your credentials:
   ```env
   HUGGINGFACE_API_KEY=your_hugging_face_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Option B: Streamlit Secrets Manager (Recommended for Deployment)
If deploying to Streamlit Community Cloud:
1. Go to your app dashboard.
2. Select **Settings** > **Secrets**.
3. Add your keys in TOML format:
   ```toml
   HUGGINGFACE_API_KEY = "your_hugging_face_token_here"
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

### Option C: UI Key Manager (Dynamic Override)
You can directly paste your tokens inside the **🔑 API Credentials Manager** inside the app sidebar. These keys are only stored in memory during your active session.

---

## 🌐 How to Deploy

### Deploying to Streamlit Community Cloud (Easiest & Free)
1. Commit your codebase to a public GitHub repository.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **New app**, select your repository, branch, and `app.py` as the entrypoint.
4. Click **Advanced settings...** to add your Secrets (keys).
5. Click **Deploy!**

---

## ⚠️ Known Limitations

- **Session-bound Memory:** Because this app runs purely in Streamlit, all generated prompt history, gallery images, and cached configurations are stored in Streamlit's `session_state`. When you refresh the webpage, close the browser, or when the server restarts, your generated history is cleared.
