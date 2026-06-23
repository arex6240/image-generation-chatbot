import streamlit as st
import io
import time
from PIL import Image

# Set up page configurations
st.set_page_config(
    page_title="ImagineAI - Image Generation Chatbot",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import our custom modules
from src.prompts import get_style_names, get_style_info, get_random_prompt
from src.api import generate_image, get_api_key, HF_API_KEY_ENV, OPENAI_API_KEY_ENV
from src.ui import inject_custom_css, render_header, render_footer, render_history_card

# Inject custom styles for premium visual appeal
inject_custom_css()

# Render top header banner
render_header()

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state.history = []
if "prompt_input_val" not in st.session_state:
    st.session_state.prompt_input_val = ""
if "last_generated" not in st.session_state:
    st.session_state.last_generated = None

# Sidebar Configuration
with st.sidebar:
    st.markdown('<h2 style="margin-top: 0;">⚙️ Settings</h2>', unsafe_allow_html=True)
    
    # 1. API Provider Selector
    st.markdown("### API Provider")
    provider = st.selectbox(
        "Choose Model Provider:",
        options=["pollinations", "huggingface", "openai"],
        format_func=lambda x: {
            "pollinations": "Pollinations.ai (Free, Fast, No Key)",
            "huggingface": "Hugging Face (Free Token, FLUX)",
            "openai": "OpenAI DALL-E 3 (Paid Key)"
        }[x]
    )
    
    # 2. Dynamic API Key inputs
    with st.expander("🔑 API Credentials Manager", expanded=False):
        st.write("Keys loaded from `.env` are used automatically. You can also paste keys below:")
        
        user_hf_key = st.text_input(
            "Hugging Face API Token:",
            type="password",
            placeholder="hf_..." if not get_api_key("huggingface") else "🔑 Loaded from environment"
        )
        
        user_openai_key = st.text_input(
            "OpenAI API Key:",
            type="password",
            placeholder="sk-..." if not get_api_key("openai") else "🔑 Loaded from environment"
        )
        
    # Store override keys in session state if provided
    hf_key_to_use = user_hf_key if user_hf_key else get_api_key("huggingface")
    openai_key_to_use = user_openai_key if user_openai_key else get_api_key("openai")
    
    # Check credentials status
    if provider == "huggingface" and not hf_key_to_use:
        st.warning("⚠️ Hugging Face key is not set. Add it in credentials or .env file.")
    elif provider == "openai" and not openai_key_to_use:
        st.warning("⚠️ OpenAI API key is not set. Add it in credentials or .env file.")
        
    st.markdown("---")
    
    # 3. Generation Options
    st.markdown("### Parameters")
    
    image_size = st.selectbox(
        "Aspect Ratio / Resolution:",
        options=["1024x1024", "1280x720", "720x1280"],
        format_func=lambda x: {
            "1024x1024": "1:1 Square (1024x1024)",
            "1280x720": "16:9 Landscape (1280x720)",
            "720x1280": "9:16 Portrait (720x1280)"
        }[x]
    )
    
    num_images = st.slider("Number of Images:", min_value=1, max_value=4, value=1)
    
    negative_prompt = st.text_input(
        "Global Negative Prompt:",
        placeholder="blurry, low quality, deformed anatomy...",
        help="Specify what you DO NOT want to see in the image."
    )
    
    seed = st.number_input(
        "Seed (for reproducibility):",
        value=0,
        step=1,
        help="Use 0 or leave empty for random seeds.",
        format="%d"
    )
    
    actual_seed = seed if seed > 0 else None

# Main Screen layout using Tabs
tab_create, tab_gallery = st.tabs(["✨ Generate Image", "🖼️ Gallery & History"])

with tab_create:
    col_input, col_output = st.columns([1.1, 0.9], gap="large")
    
    with col_input:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ✍️ Step 1: Craft Your Prompt")
        
        # Surprise me button to randomize prompt
        col_surprise, _ = st.columns([1, 1])
        with col_surprise:
            if st.button("🎲 Surprise Me! (Random Prompt)", use_container_width=True):
                st.session_state.prompt_input_val = get_random_prompt()
                st.rerun()
                
        # Main text prompt input
        prompt = st.text_area(
            "What do you want to imagine?",
            value=st.session_state.prompt_input_val,
            placeholder="A futuristic Indian city at night with flying cars and holographic ads...",
            height=120,
            help="Describe the scene in detail. Be as descriptive as possible."
        )
        # Update session state text value whenever edited
        st.session_state.prompt_input_val = prompt
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎨 Step 2: Choose an Artistic Style")
        
        # Retrieve all styled names
        style_list = get_style_names()
        selected_style = st.radio(
            "Select a style overlay:",
            options=style_list,
            index=0,
            help="This modifies the prompt to force a specific style overlay."
        )
        
        # Display style description
        style_desc = get_style_info(selected_style)["description"]
        st.info(f"💡 **{selected_style}**: {style_desc}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Big generate button
        generate_btn = st.button("🚀 Render My Imagination", type="primary")
        
    with col_output:
        st.markdown("### 🖼️ Output Preview")
        
        if generate_btn:
            if not prompt.strip():
                st.error("⚠️ Please enter a prompt first before rendering!")
            else:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                
                # Dynamic generation loop based on how many images were requested
                images_generated = []
                final_prompt = ""
                
                with st.spinner("✨ Weaving pixels... Please wait..."):
                    try:
                        for idx in range(num_images):
                            # Set distinct seeds for multiple images if seed is None
                            curr_seed = actual_seed + idx if actual_seed is not None else None
                            
                            # Run generation
                            # We supply credentials dynamically if overridden in UI
                            if provider == "huggingface":
                                img, final_prompt = generate_image(
                                    prompt=prompt,
                                    style_name=selected_style,
                                    provider=provider,
                                    size=image_size,
                                    negative_prompt=negative_prompt,
                                    seed=curr_seed
                                )
                            elif provider == "openai":
                                img, final_prompt = generate_image(
                                    prompt=prompt,
                                    style_name=selected_style,
                                    provider=provider,
                                    size=image_size,
                                    negative_prompt=negative_prompt,
                                    seed=curr_seed
                                )
                            else: # Pollinations
                                img, final_prompt = generate_image(
                                    prompt=prompt,
                                    style_name=selected_style,
                                    provider=provider,
                                    size=image_size,
                                    negative_prompt=negative_prompt,
                                    seed=curr_seed
                                )
                            
                            images_generated.append(img)
                            
                            # Save to session history list
                            st.session_state.history.append({
                                "original_prompt": prompt,
                                "final_prompt": final_prompt,
                                "style": selected_style,
                                "provider": provider,
                                "size": image_size,
                                "image": img,
                                "timestamp": time.strftime("%H:%M:%S")
                            })
                            
                        st.session_state.last_generated = {
                            "images": images_generated,
                            "final_prompt": final_prompt,
                            "original_prompt": prompt,
                            "style": selected_style,
                            "provider": provider,
                            "size": image_size
                        }
                        st.success("🎉 Render complete!")
                        
                    except Exception as e:
                        st.error(f"❌ Error during generation: {str(e)}")
                        
                st.markdown("</div>", unsafe_allow_html=True)
                
        # Display the output results
        if st.session_state.last_generated:
            output_data = st.session_state.last_generated
            images = output_data["images"]
            
            # Show a grid of images
            if len(images) == 1:
                st.markdown('<div class="image-wrapper">', unsafe_allow_html=True)
                st.image(images[0], use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Save download link
                img_bytes = io.BytesIO()
                images[0].save(img_bytes, format="PNG")
                st.download_button(
                    label="📥 Download PNG",
                    data=img_bytes.getvalue(),
                    file_name=f"imagine_{int(time.time())}.png",
                    mime="image/png",
                    key="dl_single"
                )
            else:
                # Calculate grid columns (2 per row for neatness)
                cols_per_row = 2
                for i in range(0, len(images), cols_per_row):
                    row_images = images[i:i + cols_per_row]
                    cols = st.columns(len(row_images))
                    for col_idx, img_item in enumerate(row_images):
                        with cols[col_idx]:
                            st.markdown('<div class="image-wrapper">', unsafe_allow_html=True)
                            st.image(img_item, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            img_bytes = io.BytesIO()
                            img_item.save(img_bytes, format="PNG")
                            st.download_button(
                                label=f"📥 Download #{i + col_idx + 1}",
                                data=img_bytes.getvalue(),
                                file_name=f"imagine_{int(time.time())}_{i+col_idx+1}.png",
                                mime="image/png",
                                key=f"dl_{i+col_idx}"
                            )
            
            # Detailed Info box
            with st.expander("🔍 Generation Metadata & Expanded Prompt", expanded=False):
                st.markdown(f"**Original Request:** `{output_data['original_prompt']}`")
                st.markdown(f"**Style Layer Applied:** `{output_data['style']}`")
                st.markdown(f"**Final Expanded Prompt Sent to AI:**")
                st.info(output_data['final_prompt'])
                st.code(f"Size: {output_data['size']} | Provider: {output_data['provider'].upper()}")
        else:
            # Welcome image / placeholder until the user makes a request
            st.info("🎨 Your masterpiece will appear here. Try typing a prompt on the left and hitting 'Render My Imagination'.")

with tab_gallery:
    st.markdown("### 📚 Prompt History & Output Gallery")
    
    if not st.session_state.history:
        st.write("No images generated in this session yet. Start creating above!")
    else:
        # Loop backwards through history to show newest first
        for idx, item in enumerate(reversed(st.session_state.history)):
            col_meta, col_img = st.columns([3, 1], gap="medium")
            
            with col_meta:
                render_history_card(
                    original_prompt=item["original_prompt"],
                    final_prompt=item["final_prompt"],
                    style=item["style"],
                    provider=item["provider"],
                    size=item["size"]
                )
                
                # Ability to reload the prompt back into the generator
                if st.button(f"🔄 Reload prompt #{len(st.session_state.history) - idx}", key=f"reload_{idx}"):
                    st.session_state.prompt_input_val = item["original_prompt"]
                    st.rerun()
                    
            with col_img:
                st.image(item["image"], use_container_width=True)
            
            st.markdown("<hr style='opacity: 0.1;'>", unsafe_allow_html=True)

# Render footer
render_footer()
