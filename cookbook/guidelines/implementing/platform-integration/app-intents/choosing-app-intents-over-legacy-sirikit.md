
- For new work, prefer the App Intents framework. The older SiriKit Intents (Intents.framework, `.intentdefinition` files, intent extensions) remains for specific domains (messaging, payments, CarPlay-style domains) but is legacy for general app actions.
- Do **NOT** add a new SiriKit custom intent for an action that App Intents can express; migrate existing custom intents when touched.

