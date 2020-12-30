OctoPrint Grafana Annotations Plugin
=====================================

Send [Annotations](https://grafana.com/docs/grafana/latest/dashboards/annotations/) to Grafana to mark the begin and end times of your print jobs.  This relies on the [Grafana Annotations HTTP API](https://grafana.com/docs/grafana/latest/http_api/annotations/)

I use the [Octoprint Prometheus Exporter](https://github.com/tg44/OctoPrint-Prometheus-Exporter) plugin to gather stats from my prints into [Prometheus](https://prometheus.io/), and I use [Grafana](https://grafana.com/) to view them.  This plugin directly communicates with Grafana to create timed annotations for the print jobs, which I can overlay onto the other plots.

Operation
---------

When a print job is started, a simple annotation will be sent to Grafana to mark the start of the job.  Once the job is either cancelled or completes normally, an update will be sent on the same annotation to give it an end time and the configured outcome tags.

Configuration
-------------

Install it into your [OctoPrint](https://octoprint.org/) instance, and fill out the settings page with your server info.

You'll have to go into your Grafana settings page to generate an API key for this plugin to use.

It is also highly recommended that you fill in some tags to send on the annotations that identify 
the printer etc. in case you have multiple printers.

