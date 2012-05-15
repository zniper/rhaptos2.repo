
import fabric

#absolutely and utterly needs replacing with ssh keys...RealSoonNow
try:
    fabric.state.env['user']= 'deployagent'
    fabric.state.env['password']= 'deployagent'
except Exception, e:
    print 'Avoiding raising this: %s' % e

    
