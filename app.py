import gradio as gr
from predict import FEATURES, predict_record

def predict(*values):
    try:
        result = predict_record(dict(zip(FEATURES, values)))
    except (ValueError, TypeError) as exc:
        raise gr.Error(str(exc)) from exc
    label = 'Default (1)' if result['prediction'] else 'No default (0)'
    return f"{label}\nEstimated default probability: {result['default_probability']:.2%}\nDecision threshold: 50%"

defaults = {c: 0 for c in FEATURES}
defaults.update(LIMIT_BAL=100000, SEX=2, EDUCATION=2, MARRIAGE=1, AGE=35)
demo = gr.Interface(
    fn=predict,
    inputs=[gr.Number(label=c, value=defaults[c]) for c in FEATURES],
    outputs=gr.Textbox(label='Prediction'),
    title='Credit Risk Prediction — Module 10',
    description='Course demonstration using Module 8 Trial 4. Enter a fictional client profile. '
        'Amounts are in NT dollars. SEX: 1 male, 2 female; EDUCATION: 1 graduate, 2 university, '
        '3 high school, 4 other, 0/5/6 unknown; MARRIAGE: 1 married, 2 single, 3 other, 0 unknown. '
        'Repayment fields use original dataset codes (-2 through 8). '
        'BILL_AMT1/PAY_AMT1 and PAY_0 refer to the most recent month. '
        'This model estimate is not a lending recommendation.',
    flagging_mode='never',
)
if __name__ == '__main__':
    demo.launch(server_name='0.0.0.0', server_port=7860, share=False)
