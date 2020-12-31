# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.events import Events

# requests lib seems to be part of base octoprint
import requests
import time

class GrafanaAnnotationsPlugin(octoprint.plugin.EventHandlerPlugin,
                              octoprint.plugin.TemplatePlugin,
                              octoprint.plugin.SettingsPlugin):
    def __init__(self):
        self.currentAnnotationId = None

    ##############
    ## Overrides
    ##############

    def get_settings_defaults(self):
        return dict(url='https://mygrafana:3000',
                api_key='changeme',
                dashboard_id='',
                panel_id='',
                tags='printjob, printer_mk3s',
                successTags='printjob_succeeded',
                failTags='printjob_failed',
                http_timeout=5)

    def get_template_configs(self):
        return [
            dict(type="settings", name="Grafana Annotations", custom_bindings=False)
        ]

    def on_event(self, event, payload):
        self._logger.debug("Received event %s" % event)
        if event == Events.PRINT_STARTED:
            self.begin_print_annotation(payload)
        elif event in [Events.PRINT_FAILED, Events.PRINT_CANCELLED]:
            self.end_print_annotation(False, payload)
        elif event == Events.PRINT_DONE:
            self.end_print_annotation(True, payload)
        # do we care about PRINT_PAUSED/RESUMED ?

    def get_update_information(self):
        return dict(
                GrafanaAnnotations=dict(
                    displayName="Grafana Annotations",
                    displayVersion=self._plugin_version,
                    type="github_release",
                    user="nathanic",
                    repo="OctoPrint-Printoid",
                    current=self._plugin_version,
                    pip="https://github.com/nathanic/OctoPrint-GrafanaAnnotations/archive/{target_version}.zip"
                )
            )

    ############################
    ## Santa's Little Helpers
    ############################

    def begin_print_annotation(self, payload):
        # this bit was inspired by grafannotate
        # https://github.com/devopsmakers/python-grafannotate
        ann = {'text': 'Print of %s' % payload['path'],
                'time': int(round(time.time() * 1000)),
                'tags': self.get_tags()
                }
        self._logger.info(self._settings.get(['url']))
        if self._settings.get(['dashboard_id']) != '':
            ann['dashboardId'] = self._settings.get(['dashboard_id'])
        if self._settings.get(['panel_id']) != '':
            ann['panelId'] = self._settings.get(['panel_id'])

        self._logger.info('Creating Grafana Annotation with content %s' % (ann))
        response = requests.post(self.get_api_url(), json=ann, headers=self.get_headers(), timeout=self._settings.get_int(['http_timeout']))

        if response.ok:
            result = response.json()
            if 'id' in result:
                self.currentAnnotationId = result['id']
            if 'message' in result:
                self._logger.debug('Response from Grafana: %s' % result['message'])
            self._logger.info('Grafana Annotation has ID %s' % self.currentAnnotationId)
        else:
            self._logger.error('Failed posting to grafana with response %s' % response.json)

    # patch the current annotation with the end time information and outcome tags
    def end_print_annotation(self, success, payload):
        if self.currentAnnotationId is None:
            # this will normally happen for a cancel, when Done gets called after
            self._logger.debug("Can't update grafana annotation because we don't have a current ID")
            return

        end_time = time.time()
        ann = { 'time': unixtime_to_javatime(end_time - payload['time']),
                'timeEnd': unixtime_to_javatime(end_time),
                'tags': self.get_tags(success) }
        self._logger.info('Patching Grafana Annotation ID %d with content %s' % (self.currentAnnotationId, ann))
        url = '%s/%d' % (self.get_api_url(), self.currentAnnotationId)
        response = requests.patch(url, headers=self.get_headers(), json=ann, timeout=self._settings.get_int(['http_timeout']))
        self.currentAnnotationId = None
        self._logger.info('Grafana Annotation API Response: %s' % response.json())

    def get_headers(self):
        return { 'Authorization': 'Bearer ' + self._settings.get(['api_key']),
                 'Accept': 'application/json',
                 'Content-Type': 'application/json'
                }

    def get_api_url(self):
        return self._settings.get(['url']) + '/api/annotations'

    def get_tags(self,success=None):
        tags = splip(self._settings.get(['tags']))
        if success == True:
            tags += splip(self._settings.get(['successTags']))
        elif success == False:
            tags += splip(self._settings.get(['failTags']))
        return tags

def splip(s):
    return [ t.strip() for t in s.split(',') ]

def unixtime_to_javatime(t):
    return int(round( t * 1000))

__plugin_pythoncompat__ = ">=2.7,<4"
def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = GrafanaAnnotationsPlugin()
    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
