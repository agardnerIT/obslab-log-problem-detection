--8<-- "snippets/bizevent-introduce-system-change.js"

The application is running correctly. It is time to introduce a change into the system.

This simulates releasing new functionality to your users in production.

## Inform Dynatrace

First, inform Dynatrace that a change is about to occur.
Namely, you are going to make a change to the `cart` service 
by changing the `cartFailure` feature flag from `off` to `on`.

Tell Dynatrace about the upcoming change by sending an event (note: This event does **not** actually make the change; you need to do this).

Run the following:

``` {"name": "send configuration change event to Dynatrace"}
./runtimeChange.sh cart cartFailure on
```

Refresh the `cart` page and near the bottom you should see the configuration change event.

![configuration changed event](images/configuration-change-event.png)

## Make Change

Run this script which will change the `defaultValue` of `cartServiceFailure` from `"off"` to `"on"`:

``` { "name": "write new flags" }
python3 /workspaces/REPOSITORY_NAME/write_new_flags.py
```

Now apply the change and allow the feature flag backend to re-read them by running this command:

``` { "name": "apply new flags and scale flagd"}
kubectl apply -f $CODESPACE_VSCODE_FOLDER/new_flags.yaml
kubectl scale deploy/flagd --replicas=0
kubectl scale deploy/flagd --replicas=1
```

You should see:

```
configmap/my-otel-demo-flagd-config configured
deployment/fladg scaled
deployment/fladg scaled
```

!!! warning "Be Patient"
    The application will now generate errors when emptying the users cart.
    It will do this 1/10th of the time, so be patient, it can take a few moments for the errors to occur.

## Generate Your Own Traffic

There is a load generator running, but you can generate traffic by accessing the site.

See [access user interface](access-ui.md){target=_blank}

Repeatedly add an item to your cart, go to the cart and empty it. Hope you're "lucky" that you generate a backend failure.

## Open Problems App

In a notebook, use the following DQL query to search for the relevant problem record.
As mentioned above, the app will take some time to generate the error thus expect this DQL to return 0 results for a few moments:

``` {"name": "fetch problems with dql"}
fetch events, from: now()-30m, to: now()
| filter event.kind == "DAVIS_PROBLEM"
| filter event.status_transition == "CREATED"
| filter matchesPhrase(event.name, "Critical Redis connection error!")
```

When a problem record appears, click any field then `Open record with...` and choose the `Problems` app.

<div class="grid cards" markdown>
- [Click Here to Continue :octicons-arrow-right-24:](review-problem.md)
</div>
