from flask import Flask, request, jsonify
from flask_cors import CORS
from app.agents.research_plans import create_market_research_plan, create_content_gap_analysis_plan
from app.agents.content_plans import create_content_planning_system, create_article_writing_system, create_fact_checking_system
from app.agents.podcast_plans import create_podcast_production_system
from app.agents.video_plans import create_video_production_system
from app.agents.publishing_plans import create_notion_publisher
import app
import os
import json
from app.core.portia_client import PortiaClient

app = Flask(__name__)
CORS(app) 
client = PortiaClient()

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Portia ADS API is running"})

@app.route("/api/market-research", methods=["POST"])
def market_research():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ["topic", "target_audience"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        plan = create_market_research_plan()
        result = client.run_plan2(plan, plan_run_inputs=data)
        
        # Get research reports folder contents
        research_reports = {}
        research_folder = "research_reports"
        if os.path.exists(research_folder):
            for filename in os.listdir(research_folder):
                file_path = os.path.join(research_folder, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if filename.endswith('.json'):
                                if content.strip():
                                    try:
                                        research_reports[filename] = json.loads(content)
                                    except json.JSONDecodeError as json_err:
                                        research_reports[filename] = {
                                            "error": f"Invalid JSON format: {str(json_err)}",
                                            "raw_content": content[:500] + "..." if len(content) > 500 else content
                                        }
                                else:
                                    research_reports[filename] = {"error": "Empty JSON file"}
                            else:
                                research_reports[filename] = content
                    except Exception as e:
                        research_reports[filename] = f"Error reading file: {str(e)}"
        
        return jsonify({
            "result": result,
            "research_reports": research_reports
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/content-gap-analysis", methods=["POST"])
def content_gap_analysis():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        plan = create_content_gap_analysis_plan()
        result = client.run_plan2(plan, plan_run_inputs=data)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/content-planning", methods=["POST"])
def content_planning():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Auto-load research summary from research_reports folder
        research_summary = ""
        research_folder = "research_reports"
        if os.path.exists(research_folder):
            # Look for text files first, then JSON files
            for filename in os.listdir(research_folder):
                if filename.endswith('.txt'):
                    file_path = os.path.join(research_folder, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            research_summary = f.read()
                            break
                    except Exception as e:
                        continue
            
            # If no text file found, try JSON files
            if not research_summary:
                for filename in os.listdir(research_folder):
                    if filename.endswith('.json'):
                        file_path = os.path.join(research_folder, filename)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if content.strip():
                                    research_summary = content
                                    break
                        except Exception as e:
                            continue
        
        # Use auto-loaded research summary or provided one
        if not research_summary and "research_summary" not in data:
            return jsonify({"error": "No research summary found in research_reports folder and none provided"}), 400
        
        if research_summary:
            data["research_summary"] = research_summary
        
        # Validate required fields
        required_fields = ["content_goals"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        plan = create_content_planning_system()
        result = client.run_plan2(plan, plan_run_inputs=data)
        
        # Get content plans folder contents
        content_plans = {}
        content_folder = "content_plans"
        if os.path.exists(content_folder):
            for filename in os.listdir(content_folder):
                file_path = os.path.join(content_folder, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if filename.endswith('.json'):
                                if content.strip():
                                    try:
                                        content_plans[filename] = json.loads(content)
                                    except json.JSONDecodeError as json_err:
                                        content_plans[filename] = {
                                            "error": f"Invalid JSON format: {str(json_err)}",
                                            "raw_content": content[:500] + "..." if len(content) > 500 else content
                                        }
                                else:
                                    content_plans[filename] = {"error": "Empty JSON file"}
                            else:
                                content_plans[filename] = content
                    except Exception as e:
                        content_plans[filename] = f"Error reading file: {str(e)}"
        
        return jsonify({
            "result": result,
            "content_plans": content_plans,
            "research_summary_used": research_summary[:200] + "..." if len(research_summary) > 200 else research_summary
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/article-writing", methods=["POST"])
def article_writing():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields based on test
        required_fields = ["topic", "target_keywords"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        plan = create_article_writing_system()
        result = client.run_plan2(plan, plan_run_inputs=data)
        
        # Get content drafts folder contents
        content_drafts = {}
        drafts_folder = "content_drafts"
        if os.path.exists(drafts_folder):
            for filename in os.listdir(drafts_folder):
                file_path = os.path.join(drafts_folder, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if filename.endswith('.json'):
                                if content.strip():
                                    try:
                                        content_drafts[filename] = json.loads(content)
                                    except json.JSONDecodeError as json_err:
                                        content_drafts[filename] = {
                                            "error": f"Invalid JSON format: {str(json_err)}",
                                            "raw_content": content[:500] + "..." if len(content) > 500 else content
                                        }
                                else:
                                    content_drafts[filename] = {"error": "Empty JSON file"}
                            else:
                                content_drafts[filename] = content
                    except Exception as e:
                        content_drafts[filename] = f"Error reading file: {str(e)}"
        
        return jsonify({
            "result": result,
            "content_drafts": content_drafts
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/fact-checking", methods=["POST"])
def fact_checking():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields based on test
        required_fields = ["content_to_verify"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        plan = create_fact_checking_system()
        result = client.run_plan2(plan, plan_run_inputs=data)
        
        # Get fact check reports folder contents
        fact_check_reports = {}
        reports_folder = "fact_check_reports"
        if os.path.exists(reports_folder):
            for filename in os.listdir(reports_folder):
                file_path = os.path.join(reports_folder, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if filename.endswith('.json'):
                                if content.strip():
                                    try:
                                        fact_check_reports[filename] = json.loads(content)
                                    except json.JSONDecodeError as json_err:
                                        fact_check_reports[filename] = {
                                            "error": f"Invalid JSON format: {str(json_err)}",
                                            "raw_content": content[:500] + "..." if len(content) > 500 else content
                                        }
                                else:
                                    fact_check_reports[filename] = {"error": "Empty JSON file"}
                            else:
                                fact_check_reports[filename] = content
                    except Exception as e:
                        fact_check_reports[filename] = f"Error reading file: {str(e)}"
        
        return jsonify({
            "result": result,
            "fact_check_reports": fact_check_reports
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/podcast-production", methods=["POST"])
def podcast_production():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields based on test
        required_fields = ["episode_topic", "source_content"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        plan = create_podcast_production_system()
        result = client.run_plan2(plan, plan_run_inputs=data)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/video-production", methods=["POST"])
def video_production():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields based on test
        required_fields = ["video_topic", "target_platform"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        plan = create_video_production_system()
        result = client.run_plan2(plan, plan_run_inputs=data)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/publishing", methods=["POST"])
def publishing():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields based on test
        required_fields = ["content_package"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        plan = create_notion_publisher()
        result = client.run_plan2(plan, plan_run_inputs=data)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/master-pipeline", methods=["POST"])
def master_pipeline():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields based on master plan inputs
        required_fields = ["project_name", "primary_topic", "target_audience"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        plan = app.create_master_content_production_system()
        result = client.run_plan2(plan, plan_run_inputs=data)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tools", methods=["GET"])
def list_tools():
    try:
        tool_ids = client.list_tool_ids()
        return jsonify({"tools": tool_ids})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)