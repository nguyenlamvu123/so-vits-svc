import os

import streamlit as st

from inference_main import main
from coordinate_constant import \
    result, logs_44k, spkdict, spkdict_, aud___intypelist, cn_nes, tempjson, debug, \
    readfile


def main_loop():
    global paramdict

    def dehi():
        resu = os.listdir(result)
        for out___mp4 in resu:
            if not out___mp4.endswith('.flac'):
                continue
            os.remove(os.path.join(result, out___mp4))

    st.title("FAKE VOICE")

    # show at the end of page
    st.write(  # https://stackoverflow.com/questions/41732055/how-to-set-the-div-at-the-end-of-the-page
        """
        <style>
            .banner {
              width: 100%;
              height: 15%;
              position: fixed;
              bottom: 0;
              overflow:auto;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        aud___in = st.file_uploader(
            "Upload file",
            type=aud___intypelist
            )
        f0pre = st.radio(
            "Select a F0 predictor (f0 mean pooling will be enable when using crepe)",
            [
                f"{s}" for s in [
                'crepe',
                'pm',
                'dio',
                'harvest',
                'rmvpe',
                'fcpe'
            ]
            ],
            index=1,
            # captions=["Laugh out loud.", "Get the popcorn.", "Never stop learning."]
        )
        paramdict["f0_predictor"] = f0pre
        # # assert 'checkpoint_best_legacy_500_.pt' in os.listdir('pretrain')
        # # assert 'hubert_base.pt' in os.listdir('pretrain')
        # sp_enco = st.radio(
        #     "Select speech encoder",
        #     [
        #         f"{s}" for s in [
        #         'checkpoint_best_legacy_500',
        #         'hubert-soft-0d54a1f4',
        #         ]
        #     ],
        # )
        # paramdict["speech_encoder"] = sp_enco  # TODO

    with col2:
        spk_list = st.radio(
            "Select the speaker ID to use for conversion",
            [
                # ":rainbow[Comedy]",
                f"***{spkdict[spk]}***" for spk in os.listdir(logs_44k) if spk in spkdict
                # "Documentary :movie_camera:"
            ],
            # captions=["Laugh out loud.", "Get the popcorn.", "Never stop learning."]
        )
        spk_list = spk_list.replace("*", "")  # -s
        logs_44k_spklist = f"{logs_44k}{os.sep}{spkdict_[spk_list]}"
        # st.text(f"{voicedict[spk_list]}.wav")
        paramdict["config_path"] = f"{logs_44k_spklist}{os.sep}config.json"  # -c

        if not os.path.isfile(paramdict["config_path"]):
            st.write(f'{paramdict["config_path"]} does not exists')
            return None
        else:
            conf_ = readfile(file=paramdict["config_path"], mod="_r", cont=None, jso=True)
            if len(conf_['spk']) > 1:
                spk_list_ = st.radio(
                    "Select the speaker ID to use for conversion again",
                    [
                        f"***{s}***" for s in conf_['spk']
                    ],
                    # captions=["Laugh out loud.", "Get the popcorn.", "Never stop learning."]
                )
                paramdict["spk_list"] = spk_list_.replace("*", "")
            else:
                try:
                    paramdict["spk_list"] = list(conf_['spk'].keys())[0]
                except IndexError:
                    st.write(f'not found speaker in config at {paramdict["config_path"]}')
                    return None

        readfile(file=tempjson, mod="w", cont=paramdict, jso=True)
        with st.form("checkboxes", clear_on_submit=True):
            model_path = st.radio(
                "select model",
                [
                    f"***{s}***" for s in os.listdir(logs_44k_spklist) if all(
                    [
                        s.endswith('.pth'),
                        'G_' in s,
                    ]
                )
                ],
                # captions=["Laugh out loud.", "Get the popcorn.", "Never stop learning."]
            )
            if model_path is not None:
                model_path = model_path.replace("*", "")  # -m
            paramdict["model_path"] = f"{logs_44k_spklist}{os.sep}{model_path}"
            submit = st.form_submit_button('RUN!')  # https://blog.streamlit.io/introducing-submit-button-and-forms/

    paramdict["auto_predict_f0"] = False
    paramdict["feature_retrieval"] = False
    paramdict["use_spk_mix"] = False
    paramdict["second_encoding"] = False
    paramdict["clean_names"] = ''
    with col3:
        # slice_db = st.slider(
        #     "The default is -40, noisy sounds can be -30, dry sounds can be -50 to maintain breathing.",
        #     min_value=-50,
        #     max_value=-30,
        #     value=-40
        # )  # TODO
        # paramdict["slice_db"] = slice_db

        agree = st.checkbox('automatic ***pitch_prediction***, do not enable this when converting singing voices as it can cause serious pitch issues')
        if agree:
            paramdict["auto_predict_f0"] = True
            paramdict["clean_names"] += 'pitch_prediction_'
        a0gree = st.checkbox('Whether to use feature ***retrieval***. If clustering model is used, it will be disabled, and cm and cr parameters will become the index path and mixing ratio of feature retrieval')
        if a0gree:
            paramdict["feature_retrieval"] = True
            paramdict["clean_names"] += 'retrieval_'
        a1gree = st.checkbox('whether to use ***dynamic_voice_fusion***')
        if a1gree:
            paramdict["use_spk_mix"] = True
            paramdict["clean_names"] += 'dynamic_voice_fusion_'
        a2gree = st.checkbox('which involves applying an ***additional_encoding*** to the original audio before shallow diffusion. This option can yield varying results - sometimes positive and sometimes negative')
        if a2gree:
            paramdict["second_encoding"] = True
            paramdict["clean_names"] += 'additional_encoding_'

    st.sidebar.button('xóa lịch sử', on_click=dehi)
    if not submit:
        return None
    if aud___in is None:  # AttributeError: 'NoneType' object has no attribute 'name'
        st.write('upload file again!')
        return None
    paramdict["clean_names"] += f'{spkdict_[spk_list]}_{os.path.splitext(model_path)[0]}___{aud___in.name}'  # cn_nes  # -n
    tempfile = os.path.join("raw", paramdict["clean_names"])
    with open(tempfile, "wb") as f:
        f.write(aud___in.getbuffer())
    paramdict["trans"] = 0  # -t

    if debug:
        command = "python3 inference_main.py" + \
                  f''' -m "{paramdict['model_path']}"''' + \
                  f''' -c "{paramdict['config_path']}"''' + \
                  f''' -n "{paramdict["clean_names"]}"''' + \
                  f''' -t {paramdict["trans"]}''' + \
                  f''' -s "{paramdict["spk_list"]}"''' + \
                  f''' -f0p "{paramdict["f0_predictor"]}"'''  # + \
                  # f''' -sd {paramdict["slice_db"]}'''
        if paramdict["auto_predict_f0"]: command += ' -a'
        if paramdict["feature_retrieval"]: command += ' -fr'
        if paramdict["use_spk_mix"]: command += ' -usm'
        if paramdict["second_encoding"]: command += ' -se'
        st.write(command)

    paramlist = [
        '-m', paramdict['model_path'],
        '-c', paramdict['config_path'],
        '-n', paramdict["clean_names"],
        '-t', paramdict["trans"],
        '-s', paramdict["spk_list"],
        '-f0p', paramdict["f0_predictor"],
        # '-sd', paramdict["slice_db"],  # TODO
        # '-wf', 'wav',  # TODO
    ]
    if paramdict["auto_predict_f0"]: paramlist.append('-a')
    if paramdict["feature_retrieval"]: paramlist.append('-fr')
    if paramdict["use_spk_mix"]: paramlist.append('-usm')
    if paramdict["second_encoding"]: paramlist.append('-se')
    main(paramlist)

    resu = os.listdir(result)
    for out___mp4 in resu:
        if not out___mp4.endswith('.flac'):
            continue
        data = readfile(file=os.path.join(result, out___mp4), mod="rb")
        st.write(f'{out___mp4}')
        st.audio(data, format='wav')
    #     with placeholder.container():
    #         st.write(f'{out___mp4} với giọng đọc {speaker_id}')
    #         st.download_button(
    #             label="Download",
    #             data=data,
    #             file_name=out___mp4,
    #             mime='wav',
    #         )
    os.rename(tempfile, cn_nes)


paramdict: dict = dict()
if __name__ == '__main__':
    main_loop()  # streamlit run strlit.py --server.port 8502
