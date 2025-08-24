from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.research_plans import create_market_research_plan, create_content_gap_analysis_plan
from agents.content_plans import create_content_planning_system, create_article_writing_system, create_fact_checking_system
from agents.podcast_plans import create_podcast_production_system
from agents.video_plans import create_video_production_system
from agents.publishing_plans import create_multi_platform_publisher
from app import create_master_content_production_system
from core.portia_client import PortiaClient

app = Flask(__name__)
CORS(app) 
client = PortiaClient()

@app.route("/api/market-research", methods=["POST"])
def market_research():
    data = request.json
    plan = create_market_research_plan()
    result = client.run_plan2(plan, plan_run_inputs=data)
    return jsonify({"result": result})

@app.route("/api/content-gap-analysis", methods=["POST"])
def content_gap_analysis():
    data = request.json
    plan = create_content_gap_analysis_plan()
    result = client.run_plan2(plan, plan_run_inputs=data)
    return jsonify({"result": result})

@app.route("/api/content-planning", methods=["POST"])
def content_planning():
    data = request.json
    plan = create_content_planning_system()
    result = client.run_plan2(plan, plan_run_inputs=data)
    return jsonify({"result": result})

@app.route("/api/article-writing", methods=["POST"])
def article_writing():
    data = request.json
    plan = create_article_writing_system()
    result = client.run_plan2(plan, plan_run_inputs=data)
    return jsonify({"result": result})

@app.route("/api/fact-checking", methods=["POST"])
def fact_checking():
    data = request.json
    plan = create_fact_checking_system()
    result = client.run_plan2(plan, plan_run_inputs=data)
    return jsonify({"result": result})

@app.route("/api/podcast-production", methods=["POST"])
def podcast_production():
    data = request.json
    plan = create_podcast_production_system()
    result = client.run_plan2(plan, plan_run_inputs=data)
    return jsonify({"result": result})

@app.route("/api/video-production", methods=["POST"])
def video_production():
    data = request.json
    plan = create_video_production_system()
    result = client.run_plan2(plan, plan_run_inputs=data)
    return jsonify({"result": result})

@app.route("/api/publishing", methods=["POST"])
def publishing():
    data = request.json
    plan = create_multi_platform_publisher()
    result = client.run_plan2(plan, plan_run_inputs=data)
    return jsonify({"result": result})

@app.route("/api/master-pipeline", methods=["POST"])
def master_pipeline():
    data = request.json
    plan = create_master_content_production_system()
    result = client.run_plan2(plan, plan_run_inputs=data)
    return jsonify({"result": result})

@app.route("/api/tools", methods=["GET"])
def list_tools():
    tool_ids = client.list_tool_ids()
    return jsonify({"tools": tool_ids})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)