import {registerRoot, Composition} from 'remotion';
import {Captions} from './Captions';
const Root=()=> <Composition id="BJCaptions" component={Captions} durationInFrames={150} fps={30} width={1080} height={1920}
  defaultProps={{words:["घुटने","का","दर्द","हर","बार","घिसाव","नहीं","होता"],en:"Knee pain is not always wear and tear"}}/>;
registerRoot(Root);
