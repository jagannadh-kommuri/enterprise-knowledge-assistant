# Incident response handbook — fictional demonstration data

For a severity one incident, the on-call engineer acknowledges the alert within five minutes and opens an incident channel. The incident commander coordinates investigation and publishes updates every fifteen minutes. The first priority is restoring service safely.

A rollback requires the last known healthy release, a recorded incident identifier, and approval from the incident commander. After rollback, verify API error rates, request latency, and database connection health for ten minutes before closing the incident.

A blameless postmortem is completed within three business days. Include the timeline, customer impact, root cause, contributing factors, and action items with owners and due dates. Never paste customer data or credentials into the incident channel.
