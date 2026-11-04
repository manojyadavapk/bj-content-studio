import {bundle} from '@remotion/bundler';
import {renderMedia,selectComposition} from '@remotion/renderer';
const exe='/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const serveUrl=await bundle({entryPoint:new URL('./src/index.jsx',import.meta.url).pathname});
const composition=await selectComposition({serveUrl,id:'BJCaptions',browserExecutable:exe});
await renderMedia({composition,serveUrl,codec:'h264',outputLocation:'out/test_captions.mp4',browserExecutable:exe,concurrency:2});
console.log('done');
