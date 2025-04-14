

SERVICES := app client grpc_server db


dev:
	docker compose up --build


test:
	docker compose exec client poetry run python client/entire_flow.py


database:
	docker compose exec db psql -U postgres -d library_service -c "SELECT * FROM member;"
	docker compose exec db psql -U postgres -d library_service -c "SELECT * FROM book;"
	docker compose exec db psql -U postgres -d library_service -c "SELECT * FROM borrow;"


down:
	docker compose down


clean:
	docker compose down -v --rmi all --remove-orphans

