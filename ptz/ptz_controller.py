from onvif import ONVIFCamera
from time import sleep

def media_profile_configuration(direction):
    
    # Create the media service
    mycam = ONVIFCamera("192.168.0.5", 80, "admin", "imrindi8922")
    media_service = mycam.create_media_service()
    # Create ptz service
    ptz = mycam.create_ptz_service()
    
    # Get target profile
    media_profile = media_service.GetProfiles()[0]
    
    print("Device Model : %s" % mycam.devicemgmt.GetDeviceInformation()["Model"])
    print("Network MAC addrress : %s\n\n"% mycam.devicemgmt.GetNetworkInterfaces()[0]["Info"]["HwAddress"])
    #print("GetStreamURI : %s"% media_service.GetStreamUri({'StreamSetup':{'Stream':'RTP-Unicast','Transport':'HTTP'},'ProfileToken': media_profile.token}))
    #media_service.GetSnapshotUri({'ProfielToken': media_profile.token})
    if mycam.devicemgmt.GetCapabilities()['PTZ'] is None :
        print("PTZ Not Support")
        return False
    else :
        # Get ptz configuration
        request = ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = media_profile.PTZConfiguration.token
        ptz_configuration_options = ptz.GetConfigurationOptions(request)
    
        moverequest = ptz.create_type('ContinuousMove')
        moverequest.ProfileToken = media_profile.token
    
        if moverequest.Velocity is None:
            moverequest.Velocity = ptz.GetStatus({'ProfileToken': media_profile.token}).Position

            XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
            XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
            YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
            YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min
            #Get PTZ status
    
            if direction == "u":
                moverequest.Velocity.PanTilt.x = 0
                moverequest.Velocity.PanTilt.y = 0.5
                ptz.ContinuousMove(moverequest)
                print(ptz.GetStatus({'ProfileToken': media_profile.token}))
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})
        
            elif direction == "d":
                moverequest.Velocity.PanTilt.x = 0
                moverequest.Velocity.PanTilt.y = -0.5
                ptz.ContinuousMove(moverequest)
                print(ptz.GetStatus({'ProfileToken': media_profile.token}))
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})
            elif direction == "l":
                moverequest.Velocity.PanTilt.x = -0.5
                moverequest.Velocity.PanTilt.y = 0
                ptz.ContinuousMove(moverequest)
                print(ptz.GetStatus({'ProfileToken': media_profile.token}))
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})

            elif direction == "r":
                moverequest.Velocity.PanTilt.x = 0.5
                moverequest.Velocity.PanTilt.y = 0
                ptz.ContinuousMove(moverequest)
                print(ptz.GetStatus({'ProfileToken': media_profile.token}))
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})
            elif direction == "ul":
                moverequest.Velocity.PanTilt.x = -0.5
                moverequest.Velocity.PanTilt.y = 0.5
                ptz.ContinuousMove(moverequest)
                print(ptz.GetStatus({'ProfileToken': media_profile.token}))
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})
            elif direction == "ur":
                moverequest.Velocity.PanTilt.x = 0.5
                moverequest.Velocity.PanTilt.y = 0.5
                ptz.ContinuousMove(moverequest)
                print(ptz.GetStatus({'ProfileToken': media_profile.token}))
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})
            elif direction == "dl":
                moverequest.Velocity.PanTilt.x = -0.5
                moverequest.Velocity.PanTilt.y = -0.5
                ptz.ContinuousMove(moverequest)
                print(ptz.GetStatus({'ProfileToken': media_profile.token}))
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})
            elif direction == "dr":
                moverequest.Velocity.PanTilt.x = -0.5
                moverequest.Velocity.PanTilt.y = 0.5
                ptz.ContinuousMove(moverequest)
                print(ptz.GetStatus({'ProfileToken': media_profile.token}))
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})
            elif direction == "i":
                request.Velocity.Zoom.x = 0.5
                request.Velocity.PanTilt.x = 0
                request.Velocity.PanTilt.y = 0
                ptz.ContinuousMove(moverequest)
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})
            elif direction == "o":
                request.Velocity.Zoom.x = -0.5
                request.Velocity.PanTilt.x = 0
                request.Velocity.PanTilt.y = 0
                ptz.ContinuousMove(moverequest)
                sleep(1.0)
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})

            elif direction == "s":
                ptz.Stop({'ProfileToken': moverequest.ProfileToken})
            else:
                print("Type")
"""
if __name__ == '__main__':
    media_profile_configuration("l")

"""
