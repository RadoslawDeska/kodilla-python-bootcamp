import os
from decimal import Decimal, InvalidOperation, getcontext

from flask import Flask, redirect, render_template, request, session, url_for
from functions import get_json_text, parse_text, read_csv, write_csv
from pydantic import BaseModel, field_validator

# Use absolute path to ensure the right folder path
BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.urandom(16).hex()  # required by flask.session


class Rate(BaseModel):
    name: str
    code: str
    bid: Decimal
    ask: Decimal

    @field_validator("bid", "ask", mode="before")
    @classmethod
    def ensure_decimal(cls, v):
        """Ensure the field passed to initializer is converted exactly to Decimal."""
        if isinstance(v, Decimal):
            return v
        if isinstance(v, float):
            return Decimal(str(v), context=getcontext())
        if isinstance(v, str):
            return Decimal(v, context=getcontext())
        raise TypeError(f"Unsupported type for Decimal conversion: {type(v)}")

    def bid_for(self, value: Decimal) -> Decimal:
        """Convert the value at the bid rate."""
        return self.bid * value

    def ask_for(self, value: Decimal) -> Decimal:
        """Convert the value at the ask rate."""
        return self.ask * value
    
    def convert(self, value: Decimal, mode: str) -> Decimal:
        return self.ask_for(value) if mode == "buy" else self.bid_for(value)

@app.route("/", methods=["GET", "POST"])
def get_form():
    if request.method == "POST":
        selected_currency = request.form.get("currency")
        selected_mode = request.form.get("mode")
        
        try:
            raw_amount = request.form.get("amount")
            input_amount = Decimal(raw_amount) if raw_amount else Decimal(0)
        except InvalidOperation:
            app.logger.debug(f"'{raw_amount}' is not a number.")
            input_amount = Decimal(0)

        result = rates[selected_currency].convert(input_amount, selected_mode)

        # Change to int if integer-like (trailing zeros without meaning)
        if result == result.to_integral_value():
            result = int(result)
        else:
            result = result.quantize(Decimal("0.0001"))

        # Save the form in a session
        session["mode"] = selected_mode
        session["amount"] = input_amount
        session["selected_currency"] = selected_currency
        session["result"] = result

        # Refresh the page
        return redirect(url_for("get_form"))

    """Read session upon GET
    
    - use pop() to flush the data until the next POST
    - use get() to persist the data across consecutive GET
    """
    selected_mode = session.get("mode", "buy")  # don't forget the last mode, or don't use pop
    input_amount = session.pop("amount", 0)  # remember only for the POST-GET redirection
    selected_currency = session.get("selected_currency", None)  # don't forget last selection, or don't use pop
    result = session.pop("result", None)

    return render_template(
        "form.html",
        mode=selected_mode,
        currencies=sorted(rates.keys()),
        selected_currency=selected_currency,
        amount=input_amount,
        result=result,
    )


if __name__ == "__main__":
    file_location = os.path.join(BASE_FOLDER, "rates.csv")
    """Get the newest data as text for precise numbers conversion in the parse_text function.
    This has to be moved to separate process to update on the run."""
    t = get_json_text()
    d = parse_text(t)
    write_csv(file_location, d["rates"], delimiter=";")

    # Get the rates from file
    rates = read_csv(file_location, delimiter=";")
    # Operate on Rate class instead of dicts
    rates = {
        entry["code"]: Rate(
            name=entry["currency"],
            code=entry["code"],
            bid=entry["bid"],
            ask=entry["ask"],
        )
        for entry in rates
    }

    app.run(debug=True)
