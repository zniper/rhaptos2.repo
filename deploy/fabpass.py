
import fabric

#absolutely and utterly needs replacing with ssh keys...RealSoonNow

fabric.state.env['user']= 'deployagent'
fabric.state.env['password']= 'deployagent'
