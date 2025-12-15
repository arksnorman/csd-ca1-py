"""BP Calculator Flask Application with AWS X-Ray and CloudWatch Monitoring"""

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

# Setup AWS X-Ray and CloudWatch if configured
aws_region = os.environ.get("AWS_REGION", "us-east-1")
cloudwatch_enabled = (
    os.environ.get("CLOUDWATCH_ENABLED", "false").lower() == "true"
)

if cloudwatch_enabled:
    try:
        import boto3
        import watchtower
        from aws_xray_sdk.core import xray_recorder
        from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

        # Configure X-Ray for distributed tracing
        xray_recorder.configure(service="bp-calculator")
        XRayMiddleware(app, xray_recorder)

        # Configure CloudWatch Logs handler
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        cloudwatch_handler = watchtower.CloudWatchLogHandler(
            log_group="/aws/elasticbeanstalk/bp-calculator-app",
            stream_name="application",
            boto3_client=boto3.client("logs", region_name=aws_region),
        )
        logger.addHandler(cloudwatch_handler)
        app.logger.addHandler(cloudwatch_handler)

        logger.info(
            "AWS X-Ray and CloudWatch monitoring initialized successfully"
        )
        app.logger.info("AWS monitoring configured")
    except Exception as e:
        app.logger.warning(f"Failed to initialize AWS monitoring: {e}")
else:
    app.logger.warning(
        "CLOUDWATCH_ENABLED not set to 'true' - AWS monitoring disabled"
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
        bp = BloodPressure(
            systolic=form.systolic.data, diastolic=form.diastolic.data
        )

        # Extra validation: Systolic must be greater than Diastolic
        if bp.systolic <= bp.diastolic:
            form.systolic.errors.append(
                "Systolic must be greater than Diastolic"
            )
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
                "index.html",
                form=form,
                bp=bp,
                category=category,
                validated=True,
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
    return render_template(
        "health_tips.html", tips_by_category=tips_by_category
    )


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
