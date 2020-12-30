OctoPrint Grafana Annotations Plugin
=====================================

Send Annotations to Grafana to mark the begin and end times of your print jobs.  

[Annotations](https://grafana.com/docs/grafana/latest/dashboards/annotations/)
are timed event markers that can either be a discrete point in time, or be
a range with a beginning and an end.  They can also have description text, and support tags
so you can query them in your dashboards and overlay them onto your time series
plots.  

![screenshot](annotation.png)

This plugin goes great with the [OctoPrint Prometheus Exporter](https://github.com/tg44/OctoPrint-Prometheus-Exporter) 
plugin, which can give you time series data about temperatures etc. to put on your fancy dashboards as a backdrop for these annotations.

Operation
---------

When a print job is started, a discrete event annotation will be sent to
Grafana to mark the start of the job.  Once the job is either cancelled or
completes normally, an update will be sent on the same annotation to give it an
end time and the configured outcome tags.

Setup
-----

Install the plugin via the Plugin Manager or manually using this URL:

	https://github.com/nathanic/OctoPrint-GrafanaAnnotations/archive/master.zip

Settings
-------------

The settings are pretty much documented on the settings page, and I'm lazy, so here's a screenshot.

![screenshot](settings.png)

It is strongly suggested that you add an unconditional tag that identifies
which printer is responsible if you have more than one machine.

References
----------
 - [OctoPrint Plugin Tutorial](https://docs.octoprint.org/en/master/plugins/gettingstarted.html)
 - [Grafana Annotations HTTP API](https://grafana.com/docs/grafana/latest/http_api/annotations/) 
