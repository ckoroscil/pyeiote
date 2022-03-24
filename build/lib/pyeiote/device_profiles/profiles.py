__profiles = {
    "generic": {},
    "switch": {
        "tp-link": {
            "mac": "50:3e:aa"
        }
    },
    "printer": {
        "Epson": {
            "mac": "38:9d:92"
        },
        "Xerox": {
            "mac": "E8:4D:EC"
        }
    },
    "phone": {
        "Cisco": {
            "mac": "00:03:6b",
            "user-agent": [
                "CSCO/4",
                "CSCO/5"
            ]
        },
        "Siemens": {
            "mac": "00:01:e3",
            "user-agent": [
                "optiPoint 600 office MxSF/v3.5.3.4"
            ]
        },
        "Avaya": {
            "mac": "00:04:0d",
            "user-agent": [
                "Avaya one-X Deskphone",
                "Avaya SIP R2.2 Endpoint Brcm Callctrl/1.5.1.0 MxSF/v3.2.6.26"
            ]
        },
        "Polycom": {
            "mac": "00:04:F2",
            "user-agent": [
                "PolycomSoundPointIP-SPIP_450-UA/3.3.4.0085"
            ]
        },
        "Aastra": {
            "mac": "00:08:5D",
            "user-agent": [
                "Aastra 480i/1.3.0.1080 Brcm Callctrl/1.5.1 MxSF/v3.2.6.26",
                "Aastra 480i Cordless/1.3.0.1080 Brcm Callctrl/1.5.1 MxSF/v3.2.6.26",
                "Aastra 9112i/1.3.0.1080 Brcm Callctrl/1.5.1 MxSF/v3.2.6.26",
                "Aastra 9133i/1.3.0.1080 Brcm Callctrl/1.5.1 MxSF/v3.2.6.26"
                
            ]
        }
    }
}
    
def get_profiles():
    return keys_to_lower(__profiles)

def keys_to_lower(d):
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = keys_to_lower(v)
        new[k.lower()] = v
    return new
