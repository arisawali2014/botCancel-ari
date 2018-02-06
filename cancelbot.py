from linepy import *
import time

cl = LINE('EMAIL','PASS')
poll = OEPoll(cl)

while True:
    try:
        ops = poll.singleTrace(count=50)
        if ops != None:
            for op in ops:
                if (op.type == 13):
                    cl.acceptGroupInvitation(op.param1)
                    cl.sendMessage(op.param1,'Start!')
                    cl.sendMessage(op.param1,'Cancelling~')
                if (op.type == 25):
                    msg = op.message
                    if (msg.text.lower() == 'start!'):
                        s = time.time()
                        cl.sendMessage('Speed!')
                        e = time.time() - s
                        cl.sendMessage('{:.14f}'.format(e))
                    if ('cancelling~' in msg.text.lower()):
                        g = cl.getCompactGroup(msg.to)
                        mids = [i.mid for i in g.invitee]
                        for mid in mids:
                            try:
                                cl.cancelGroupInvitation(msg.to,[mid])
                            except Exception as e:
                                pass
                        cl.sendMessage(msg.to,'Done!\nline://ti/p/~arisawali2014')
                        cl.leaveGroup(msg.to)
                poll.setRevision(op.revision)
    except Exception as e:
        cl.log("[SINGLE_TRACE] ERROR : " + str(e))
