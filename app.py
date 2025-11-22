"""BP Calculator Flask Application with Application Insights Telemetry"""

import os
import logging
from flask import Flask, render_template, request
from forms import BloodPressureForm
from models.blood_pressure import BloodPressure
from models.health_tips import HealthTips

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secret123")

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 5000))
MODE = os.environ.get("MODE", "prod")

# Setup Application Insights telemetry if configured
connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")

if connection_string:
    try:
        from azure.monitor.opentelemetry import configure_azure_monitor

        # Configure Azure Monitor OpenTelemetry
        configure_azure_monitor(connection_string=connection_string)

        # Setup logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.info("Application Insights telemetry initialized successfully")
        app.logger.info("Azure Monitor OpenTelemetry configured")
    except Exception as e:
        app.logger.warning(f"Failed to initialize Application Insights: {e}")
else:
    app.logger.warning(
        "APPLICATIONINSIGHTS_CONNECTION_STRING not set - telemetry disabled"
    )


@app.route("/", methods=["GET", "POST"])
def index():
    form = BloodPressureForm()

    if request.method == "GET":
        # Set initial values
        form.systolic.data = 100
        form.diastolic.data = 60

    if form.validate_on_submit():
        # Create BloodPressure object
        bp = BloodPressure(systolic=form.systolic.data, diastolic=form.diastolic.data)

        # Extra validation: Systolic must be greater than Diastolic
        if bp.systolic <= bp.diastolic:
            form.systolic.errors.append("Systolic must be greater than Diastolic")
            app.logger.warning(
                f"Validation failed: systolic={bp.systolic} <= diastolic={bp.diastolic}"
            )
        else:
            # Get the category
            category = bp.category
            app.logger.info(
                f"BP calculated: systolic={bp.systolic}, diastolic={bp.diastolic}, category={category.value}"
            )
            return render_template(
                "index.html", form=form, bp=bp, category=category, validated=True
            )

    return render_template(
        "index.html", form=form, bp=None, category=None, validated=False
    )


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/tips")
def health_tips():
    """Health Tips - New Feature"""
    # Get tips for all categories using string keys for template
    bp_low = BloodPressure(80, 50)
    bp_ideal = BloodPressure(110, 70)
    bp_pre_high = BloodPressure(130, 85)
    bp_high = BloodPressure(150, 95)

    tips_by_category = {
        "Low Blood Pressure": HealthTips.get_tips(bp_low.category),
        "Ideal Blood Pressure": HealthTips.get_tips(bp_ideal.category),
        "Pre-High Blood Pressure": HealthTips.get_tips(bp_pre_high.category),
        "High Blood Pressure": HealthTips.get_tips(bp_high.category),
    }
    app.logger.info("Health tips page accessed")
    return render_template("health_tips.html", tips_by_category=tips_by_category)


@app.route("/favicon.ico")
def favicon():
    """Return 204 No Content for favicon requests"""
    return "", 204


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    import uuid

    request_id = str(uuid.uuid4())[:8]
    return render_template("error.html", request_id=request_id), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    import uuid

    request_id = str(uuid.uuid4())[:8]
    return render_template("error.html", request_id=request_id), 500


if __name__ == "__main__":
    app.run(debug=(MODE != "prod"), host=HOST, port=PORT)
