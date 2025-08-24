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
        
        # Get podcast episodes folder contents
        podcast_episodes = {}
        episodes_folder = "podcast_episodes"
        if os.path.exists(episodes_folder):
            for filename in os.listdir(episodes_folder):
                file_path = os.path.join(episodes_folder, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if filename.endswith('.json'):
                                if content.strip():
                                    try:
                                        podcast_episodes[filename] = json.loads(content)
                                    except json.JSONDecodeError as json_err:
                                        podcast_episodes[filename] = {
                                            "error": f"Invalid JSON format: {str(json_err)}",
                                            "raw_content": content[:500] + "..." if len(content) > 500 else content
                                        }
                                else:
                                    podcast_episodes[filename] = {"error": "Empty JSON file"}
                            else:
                                podcast_episodes[filename] = content
                    except Exception as e:
                        podcast_episodes[filename] = f"Error reading file: {str(e)}"
        
        return jsonify({
            "result": result,
            "podcast_episodes": podcast_episodes
        })
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
        
        # Extract video link from result
        video_link = None
        try:
            # Parse the result to find video URL
            if isinstance(result, dict):
                # Look for video URL in various possible locations
                for key, value in result.items():
                    if "step_" in str(key) and "output" in str(key):
                        if isinstance(value, dict) and "value" in value:
                            step_value = value["value"]
                            if isinstance(step_value, str):
                                # Parse JSON string if needed
                                try:
                                    import json as json_lib
                                    parsed_value = json_lib.loads(step_value)
                                    if isinstance(parsed_value, dict) and "content" in parsed_value:
                                        for content_item in parsed_value["content"]:
                                            if content_item.get("type") == "text":
                                                text = content_item.get("text", "")
                                                if "ai.invideo.io" in text:
                                                    video_link = text
                                                    break
                                except:
                                    # If not JSON, check if it's a direct URL
                                    if "ai.invideo.io" in step_value:
                                        video_link = step_value
                            elif "ai.invideo.io" in str(step_value):
                                video_link = str(step_value)
                        elif isinstance(value, str) and "ai.invideo.io" in value:
                            video_link = value
                
                # Also check direct result content
                if not video_link and "content" in result:
                    content = result["content"]
                    if isinstance(content, list):
                        for item in content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                text = item.get("text", "")
                                if "ai.invideo.io" in text:
                                    video_link = text
                                    break
            
            # Fallback: search in string representation
            if not video_link:
                result_str = str(result)
                import re
                url_pattern = r'https://ai\.invideo\.io/[^\s"\']*'
                matches = re.findall(url_pattern, result_str)
                if matches:
                    video_link = matches[0]
        except Exception as e:
            print(f"Error extracting video link: {e}")
        
        # Get video production folder contents
        video_production_files = {}
        video_folder = "video_production"
        if os.path.exists(video_folder):
            for filename in os.listdir(video_folder):
                file_path = os.path.join(video_folder, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if filename.endswith('.json'):
                                if content.strip():
                                    try:
                                        video_production_files[filename] = json.loads(content)
                                    except json.JSONDecodeError as json_err:
                                        video_production_files[filename] = {
                                            "error": f"Invalid JSON format: {str(json_err)}",
                                            "raw_content": content[:500] + "..." if len(content) > 500 else content
                                        }
                                else:
                                    video_production_files[filename] = {"error": "Empty JSON file"}
                            else:
                                video_production_files[filename] = content
                    except Exception as e:
                        video_production_files[filename] = f"Error reading file: {str(e)}"
        
        return jsonify({
            "result": result,
            "video_link": video_link,
            "video_production_files": video_production_files
        })
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