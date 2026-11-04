import {AbsoluteFill,useCurrentFrame,useVideoConfig,spring,interpolate} from 'remotion';
const NAVY='#0D2C5C',GREEN='#62AA94',GOLD='#E6AD3C',MINT='#E0F1EC';
export const Captions=({words,en})=>{
  const f=useCurrentFrame(),{fps}=useVideoConfig();
  const per=10; // frames per word
  return <AbsoluteFill style={{background:'linear-gradient(#24476e,#0D2C5C)'}}>
    {/* name band in first 2 s, as per NMC rules */}
    <div style={{position:'absolute',top:120,left:60,right:60,padding:'18px 28px',borderRadius:20,background:'rgba(13,44,92,.9)',
      borderLeft:`10px solid ${GREEN}`,color:'#fff',fontFamily:'Poppins, sans-serif',
      transform:`translateX(${interpolate(spring({frame:f,fps}),[0,1],[-1200,0])}px)`}}>
      <div style={{fontSize:46,fontWeight:700}}>Dr Manoj Yadav · MS (Ortho)</div>
      <div style={{fontSize:30,color:MINT}}>MMC Reg. 2017073017</div>
    </div>
    <div style={{position:'absolute',top:1060,left:60,right:60,textAlign:'center',display:'flex',flexWrap:'wrap',justifyContent:'center',gap:'0 22px'}}>
      {words.map((w,i)=>{const s=spring({frame:f-20-i*per,fps,config:{damping:12}});
        const on=f>=20+i*per&&f<20+(i+1)*per;
        return <span key={i} style={{fontFamily:'Mukta, sans-serif',fontWeight:800,fontSize:92,lineHeight:1.25,
          color:on?GOLD:'#fff',opacity:s,transform:`scale(${0.6+0.4*s})`,display:'inline-block',
          textShadow:'0 6px 18px rgba(0,0,0,.55)'}}>{w}</span>})}
      <div style={{width:'100%',marginTop:18,fontFamily:'Poppins, sans-serif',fontSize:40,color:MINT,
        opacity:interpolate(f,[20+words.length*per,30+words.length*per],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>{en}</div>
    </div>
  </AbsoluteFill>;
};
