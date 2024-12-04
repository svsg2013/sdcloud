import gradio as gr

import modules.scripts as scripts
import modules.infotext_utils as parameters_copypaste

js = """
function sdcloudLoad() {
    function parsePrompt(prompt) {
        const promptEl = document.querySelector("#sdcloud-prompt textarea");
        const parseBtn = document.querySelector("#sdcloud-parse");
    
        // console.log("promptEl: ", promptEl);
        // console.log("parseBtn: ", parseBtn);

        promptEl.value = prompt;
        promptEl.dispatchEvent(new Event("input"));
        parseBtn.click();
    
    }

    const qs = new URLSearchParams(window.location.search);

    const prompt = qs.get("sdcloud_prompt");

    if (prompt) {
        parsePrompt(prompt);
    }

    window.addEventListener("message", function (event) {
        console.log("message: ", event);

        if (event.data && event.data.type === "sdcloud-prompt") {
            parsePrompt(event.data.prompt);
        }
    });

    console.log("SDCloud loaded");
}
"""


class SDCloudScript(scripts.Script):
    def title(self):
        return "SDCloud"

    # def show(self, is_img2img):
    #     return scripts.AlwaysVisible

    def ui(self, is_img2img):
        if is_img2img:
            return

        with gr.Blocks() as block:
            with gr.Accordion("SDCloud", open=False):
                with gr.Row():
                    gen_data = gr.TextArea(elem_id="sdcloud-prompt")
                    parse_btn = gr.Button(value="Parse", elem_id="sdcloud-parse")

                    block.load(_js=js)

        parameters_copypaste.register_paste_params_button(
            parameters_copypaste.ParamBinding(
                paste_button=parse_btn,
                tabname="txt2img",
                source_text_component=gen_data,
                source_image_component=None,
            )
        )
