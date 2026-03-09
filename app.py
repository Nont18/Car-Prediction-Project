from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd 
import joblib
import pickle 

scaler = joblib.load('scaler.gz')
filename = "CPModel.pkl"
loaded_model = pickle.load(open(filename, 'rb'))

columns = [
    'year', 'km_driven', 'mileage', 'engine', 'seats',
    'brand_1', 'brand_2', 'brand_3', 'brand_4', 'brand_5', 'brand_6', 'brand_7', 'brand_8',
    'brand_9', 'brand_10', 'brand_11', 'brand_12', 'brand_13', 'brand_14', 'brand_15',
    'brand_16', 'brand_17', 'brand_18', 'brand_19', 'brand_20', 'brand_21', 'brand_22',
    'brand_23', 'brand_24', 'brand_25', 'brand_26', 'brand_27', 'brand_28', 'brand_29',
    'brand_30', 'brand_31', 'seller_type_1', 'seller_type_2', 'transmission_1',
    'owner_2', 'owner_3', 'owner_4'
]
X = pd.DataFrame(columns=columns)
cols_to_scale = ['year', 'km_driven', 'mileage', 'engine']
trained_columns = X.columns

brand_options = [
    "Maruti", "Hyundai", "Toyota", "Honda", "Ford", "Mahindra", "Tata", "Renault", "Kia", "Skoda"
]
seller_options = ["Individual", "Dealer"]
transmission_options = ["Manual", "Automatic"]
owner_options = ["First Owner","Second Owner","Third Owner","Fourth & Above Owner","Test Drive Car"]

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)

CARD_STYLE = {
    "maxWidth": "900px",
    "margin": "30px auto",
    "padding": "24px",
    "borderRadius": "12px",
    "boxShadow": "0 6px 18px rgba(0,0,0,0.12)",
    "backgroundColor": "white",
    "fontFamily": "Arial, Helvetica, sans-serif"
}
HEADER_STYLE = {"textAlign": "center", "marginBottom": "8px"}
SUB_STYLE = {"textAlign": "center", "color": "#555", "marginBottom": "20px"}
FORM_ROW = {"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px"}
FIELD_STYLE = {"display": "flex", "flexDirection": "column", "gap": "6px"}
SUBMIT_STYLE = {
    "marginTop": "14px",
    "padding": "10px 16px",
    "borderRadius": "8px",
    "border": "none",
    "cursor": "pointer",
    "fontSize": "16px",
    "backgroundColor": "#2c7be5",
    "color": "white"
}
OUTPUT_STYLE = {
    "marginTop": "18px",
    "padding": "12px",
    "borderRadius": "8px",
    "backgroundColor": "#f7f9fc",
    "textAlign": "center",
    "fontSize": "18px",
    "fontWeight": "600"
}

app.layout = html.Div([
    html.Div([
        html.H1("Car Price Prediction", style=HEADER_STYLE),
        html.P("Estimate the resale price of a used car. ปรับค่าแล้วกด Submit เพื่อทำนาย", style=SUB_STYLE),

        # form card
        html.Div([
            html.Div([
                # two-column form
                html.Div([
                    # left col
                    html.Div([
                        html.Div([
                            html.Label("Brand"),
                            dcc.Dropdown(id="input-1", options=[{"label":b,"value":b} for b in brand_options], value="Maruti", clearable=True, placeholder="Type or choose brand")
                        ], style=FIELD_STYLE),

                        html.Div([
                            html.Label("Year"),
                            dcc.Input(id="input-2", type="number", value=2014, min=1980, max=2025)
                        ], style=FIELD_STYLE),

                        html.Div([
                            html.Label("Kilometer Driven"),
                            dcc.Input(id="input-3", type="number", value=145500, min=0, step=100)
                        ], style=FIELD_STYLE),

                        html.Div([
                            html.Label("Seller Type"),
                            dcc.Dropdown(id="input-4", options=[{"label":s,"value":s} for s in seller_options], value="Individual", clearable=False)
                        ], style=FIELD_STYLE),
                    ], style={"display":"flex","flexDirection":"column","gap":"10px"}),

                ], style={"gridColumn":"1/2"}),

                html.Div([
                    # right col
                    html.Div([
                        html.Label("Transmission"),
                        dcc.Dropdown(id="input-5", options=[{"label":t,"value":t} for t in transmission_options], value="Manual", clearable=False)
                    ], style=FIELD_STYLE),

                    html.Div([
                        html.Label("Owner"),
                        dcc.Dropdown(id="input-6", options=[{"label":o,"value":o} for o in owner_options], value="First Owner", clearable=False)
                    ], style=FIELD_STYLE),

                    html.Div([
                        html.Label("Mileage (kmpl)"),
                        dcc.Input(id="input-7", type="number", value=23.4, min=0, step=0.1)
                    ], style=FIELD_STYLE),

                    html.Div([
                        html.Label("Engine (cc)"),
                        dcc.Input(id="input-8", type="number", value=1248, min=0, step=1)
                    ], style=FIELD_STYLE),

                    html.Div([
                        html.Label("Seats"),
                        dcc.Input(id="input-9", type="number", value=5, min=1, max=9)
                    ], style=FIELD_STYLE),
                ], style={"gridColumn":"2/3"}),
            ], style=FORM_ROW),

            # submit button and output
            html.Div([
                html.Button("Submit", id="submit-btn", n_clicks=0, style=SUBMIT_STYLE),
                html.Div(id="number-output", style=OUTPUT_STYLE)
            ], style={"display":"flex", "justifyContent":"space-between", "alignItems":"center", "gap":"12px", "marginTop":"18px", "flexWrap":"wrap"})
        ], style=CARD_STYLE),
    ], style={"padding":"12px"})
], style={"backgroundColor":"#f0f2f6", "minHeight":"100vh"})


@callback(
    Output("number-output", "children"),
    Input("submit-btn", "n_clicks"),
    Input("input-1", "value"),
    Input("input-2", "value"),
    Input("input-3", "value"),
    Input("input-4", "value"),
    Input("input-5", "value"),
    Input("input-6", "value"),
    Input("input-7", "value"),
    Input("input-8", "value"),
    Input("input-9", "value"),
)
def update_output(n_clicks, input1, input2, input3, input4, input5, input6, input7, input8, input9):
    if n_clicks is None or n_clicks == 0:
        return "กรอกข้อมูลแล้วกด Submit เพื่อดูผลการทำนาย"

    # mapping owner
    mapping = {"First Owner":1,
               "Second Owner":2,
               "Third Owner":3,
               "Fourth & Above Owner":4,
               "Test Drive Car":5}

    new_data = pd.DataFrame([{
        'brand': input1 if input1 is not None else "",
        'year': input2 if input2 is not None else 0,
        'km_driven': input3 if input3 is not None else 0,
        'seller_type': input4 if input4 is not None else "",
        'transmission': input5 if input5 is not None else "",
        'owner': input6 if input6 is not None else "",
        'mileage': input7 if input7 is not None else 0,
        'engine': input8 if input8 is not None else 0,
        'seats': input9 if input9 is not None else 0
    }])

    new_data['owner'] = new_data['owner'].map(mapping)
    new_data = pd.get_dummies(new_data, columns=['brand', 'seller_type', 'transmission', 'owner'], drop_first=True)
    new_data = new_data.reindex(columns=trained_columns, fill_value=0)
    try:
        new_data[cols_to_scale] = scaler.transform(new_data[cols_to_scale])
    except Exception as e:
        return f"Error scaling data: {e}"

    # predict
    try:
        pred = loaded_model.predict(new_data)
        price = float(pred[0])
    except Exception as e:
        return f"Error in model prediction: {e}"

    return f"Predicted Price: ฿{price:,.2f}"

if __name__ == "__main__":
    app.run(debug=True)


