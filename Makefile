api:
	CDQ__CORE__NODE=.env uvicorn cdq.analytics.api.app:app --host=0.0.0.0 --port=8081 --reload

test:
	CDQ__CORE__NODE=.env pytest -v --seed
	
