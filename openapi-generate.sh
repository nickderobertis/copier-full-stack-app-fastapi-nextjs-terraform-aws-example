relative_out_path=frontend/copier-full-stack-app-fastapi-nextjs-terraform-aws-example/lib/api/api-client

# TODO: Remove need to set these variables to run codegen
docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm \
  -e FE_URL=a -e EMAIL_USER=a -e EMAIL_PASSWORD=a -e GOOGLE_CLIENT_ID=a \
  -e GOOGLE_CLIENT_SECRET=a -e GOOGLE_JWT_SECRET=a \
  api pipenv run python -m app.generate_openapi_spec

echo "Generating TypeScript client"
docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
    -i /local/copier_full_stack_app_fastapi_nextjs_terraform_aws_example/app/openapi.json \
    -g typescript-fetch \
    -o /local/$relative_out_path \
    -c /local/ts-openapi-config.yml

if [ ! -z "$CI" ]; then
  sudo chown -R $(whoami) $relative_out_path
fi

# Workaround for https://github.com/OpenAPITools/openapi-generator/issues/4626
# First fix issues with ErrorModel
# Use sed to remove the portion of the file $relative_out_path/models/ErrorModel.tx
# that begins with export function ErrorModelFromJSON(json: any): ErrorModel { and goes until the end of the file
sed -i '/export function ErrorModelFromJSON(json: any): ErrorModel {/,$d' $relative_out_path/models/ErrorModel.ts
# Now use sed to remove the ErrorModelFromJSON, and ErrorModelToJSON, lines from any files in the $relative_out_path/apis folder
sed -i '/ErrorModelFromJSON/,/ErrorModelToJSON/d' $relative_out_path/apis/*.ts
# Now fix issues with ValidationError
# Use sed to remove the portion of the file $relative_out_path/models/ValidationError.tx
# that begins with export function ValidationErrorFromJSON(json: any): ValidationError { and goes until the end of the file
sed -i '/export function ValidationErrorFromJSON(json: any): ValidationError {/,$d' $relative_out_path/models/ValidationError.ts
# Now remove HTTPValidationError that imports ValidationError
rm -f $relative_out_path/models/HTTPValidationError.ts
# Now use sed to remove lines referencing HTTPValidationError from any files in the $relative_out_path/apis folder
sed -i '/HTTPValidationError/d' $relative_out_path/apis/*.ts
# Now remove the export line referencing HTTPValidationError from $relative_out_path/models/index.ts
sed -i '/HTTPValidationError/d' $relative_out_path/models/index.ts
