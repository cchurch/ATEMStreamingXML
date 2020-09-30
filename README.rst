|PyPI Version| |Python Versions| |License|

ATEMStreamingXML
================

Utility to update ATEM Software Control Streaming.xml file to support new streaming providers (for use with ATEM Mini Pro and ATEM Mini Pro ISO).

Installation
------------

Install with pip::

  pip install ATEMStreamingXML

Command Line Usage
------------------

**Usage**::

  ATEMStreamingXML [-h] -S SERVICE [-N SERVER_NAME] [-U SERVER_URL]
  [--default-profiles] [-P PROFILE_NAME] [-C {1080p60,1080p30}]
  [--br BITRATE] [--abr AUDIO_BITRATE] [--ki KEYFRAME_INTERVAL]
  [--remove] [--remove-server] [--remove-profile] [--remove-config] [-n]

**Arguments**

  -h, --help            show this help message and exit
  -S SERVICE, --service SERVICE  Streaming service name to update/remove
  -N SERVER_NAME, --server-name SERVER_NAME  Streaming server name to update/remove
  -U SERVER_URL, --server-url SERVER_URL  Streaming server RTMP URL
  --default-profiles    Create or update default profiles for a streaming service
  -P PROFILE_NAME, --profile-name PROFILE_NAME  Streaming profile name to update/remove
  -C RESOLUTION, --profile-config RESOLUTION   Streaming profile config resolution and frame rate to update/remove (``1080p60`` or ``1080p30``)
  --br BITRATE, --bitrate BITRATE  Streaming profile config bitrate
  --abr AUDIO_BITRATE, --audio-bitrate AUDIO_BITRATE  Streaming profile config audio bitrate
  --ki KEYFRAME_INTERVAL, --keyframe-interval KEYFRAME_INTERVAL  Streaming profile config keyframe interval
  --remove, --remove-service  Remove streaming service
  --remove-server       Remove streaming server from a service
  --remove-profile      Remove streaming profile from a service
  --remove-config       Remove streaming profile config from a profile
  -n, --dry-run         Show changes that would be made

**Environment Variables**

  ``ATEM_STREAMING_XML``
    Specify an alternate path to the ``Streaming.xml`` file (used for unit tests)

Caveats
-------

* Does not preserve XML comments (limitation of ``xml.etree.ElementTree``).
* Does not allow reordering of streaming services, servers or profiles.
* Does not save backup copy of original ``Streaming.xml``.
* Requires running with ``sudo`` and will prompt accordingly if access is denied to modify the ``Streaming.xml``.
* Only tested on OSX.


.. |PyPI Version| image:: https://img.shields.io/pypi/v/ATEMStreamingXML.svg
   :target: https://pypi.python.org/pypi/ATEMStreamingXML
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/ATEMStreamingXML.svg
   :target: https://pypi.python.org/pypi/ATEMStreamingXML
.. |License| image:: https://img.shields.io/pypi/l/ATEMStreamingXML.svg
   :target: https://pypi.python.org/pypi/ATEMStreamingXML
