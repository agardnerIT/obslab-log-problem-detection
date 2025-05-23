#!/bin/bash
# Usage: ./runtimeChange.sh serviceName flagKey newFlagValue
# eg. ./runtimeChange.sh cart cartFailure on

echo "Changing feature flag key: $2 to $3 for service: $1"

# Build URL from parts
full_apps_url="https://${DT_ENVIRONMENT_ID}"
full_gen2_url=""

if [ "${DT_ENVIRONMENT_TYPE}" = "dev" ]; then
  echo "environment is dev"
  full_apps_url+=".dev.apps.dynatracelabs.com"
  # Remove apps.
  full_gen2_url=${full_apps_url/apps.}
elif [ "${DT_ENVIRONMENT_TYPE}" = "sprint" ]; then
  echo "environment is sprint"
  full_apps_url+=".sprint.apps.dynatracelabs.com"
  # Remove apps.
  full_gen2_url=${full_apps_url/apps.}
else
  echo "DT_ENVIRONMENT_TYPE is either 'live' or some other value. Defaulting to live"
  full_apps_url+=".apps.dynatrace.com"
  full_gen2_url=${full_apps_url/.apps./.live.}
fi

##############
# Step 1
# Inform Dynatrace that a configuration change is occurring
##############

curl -X POST "$full_gen2_url/api/v2/events/ingest" \
  -H "accept: application/json; charset=utf-8" -H "Authorization: Api-Token $DT_API_TOKEN" -H "Content-Type: application/json; charset=utf-8" \
  -d "{
    \"title\": \"feature flag changed\",
    \"entitySelector\": \"type(SERVICE),entityName.equals($1)\",
    \"eventType\": \"CUSTOM_CONFIGURATION\",
    \"properties\": {
      \"dt.event.is_rootcause_relevant\": true,
      \"action\": \"changed\",
      \"feature_flag.key\": \"$2\",
      \"defaultValue\": \"$3\"
    }
  }"

echo