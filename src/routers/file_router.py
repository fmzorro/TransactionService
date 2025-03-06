# from starlette import status
# from fastapi import APIRouter, UploadFile, HTTPException
#
# from src.services.file_parsers.parse_csv import ParseCSV
#
# file_router = APIRouter(
#     prefix="/file",
#     tags=["Parse Files"],
#     responses={404: {"description": "Not found"}},
# )
#
#
# @file_router.post("/parse/ofx/")
# def parse_ofx_file(transactions_file: UploadFile):
#     if transactions_file.content_type == "application/x-ofx":
#         # Verify file
#         try:
#             print(f"Received: {transactions_file.filename}")
#             pass
#         except Exception:
#             return HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Error parsing file.",
#             )
#
#     return HTTPException(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         detail="Only OFX files are supported.",
#     )
#
#
# @file_router.post("/parse/csv/")
# async def parse_csv_file(transactions_file: UploadFile):
#     if transactions_file.content_type == "text/csv":
#         try:
#             print(f"Received: {transactions_file.filename}")
#             contents = (await transactions_file.read()).decode("utf-8")
#             return ParseCSV(file_contents=contents).parse()
#         except Exception as e:
#             print(f"Error parsing file. Reason: {e}")
#             return HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Error parsing file.",
#             )
#         finally:
#             await transactions_file.close()
#
#     return HTTPException(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         detail="Only CSV files are supported.",
#     )
