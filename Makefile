.PHONY: run_streamlit

# Run streamlit app locally
run_streamlit:
	poetry run streamlit run app.py  --browser.gatherUsageStats False
