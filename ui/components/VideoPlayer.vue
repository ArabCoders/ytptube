<style>
:root {
  --plyr-captions-background: rgba(0, 0, 0, 0.6);
  --plyr-captions-text-color: #f3db4d;
  --webkit-text-track-display: none;
}

.plyr__caption {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
  font-size: 140%;
  font-weight: bold;
}

.plyr--full-ui ::-webkit-media-text-track-container {
  display: var(--webkit-text-track-display);
}
</style>

<template>
  <div>
    <video ref="video" :poster="thumbnail" :controls="isControls" :title="title" playsinline>
      <source :src="link" type="application/x-mpegURL" />
    </video>
  </div>
</template>

<script setup>
import { onMounted, onUpdated, ref, defineProps, defineEmits, onUnmounted } from 'vue'
import Hls from 'hls.js'
import Plyr from 'plyr'
import 'plyr/dist/plyr.css'

const props = defineProps({
  link: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: ''
  },
  thumbnail: {
    type: String,
    default: ''
  },
  artist: {
    type: String,
    default: ''
  },
  isControls: {
    type: Boolean,
    default: true
  },
})

const emitter = defineEmits(['closeModel'])

const video = ref(null)
let player = null;
let hls = null;

const eventFunc = e => {
  if (e.key === 'Escape') {
    emitter('closeModel')
  }
}

onMounted(() => {
  if (/(iPhone|iPod|iPad).*AppleWebKit/i.test(navigator.userAgent)) {
    document.documentElement.style.setProperty('--webkit-text-track-display', 'block');
  }

  prepareVideoPlayer()
  window.addEventListener('keydown', eventFunc)
})

onUpdated(() => prepareVideoPlayer())

onUnmounted(() => {
  if (player) {
    player.destroy()
  }
  if (hls) {
    hls.destroy()
  }

  window.removeEventListener('keydown', eventFunc)

  if (props.title) {
    window.document.title = 'YTPTube'
  }
})

const prepareVideoPlayer = () => {
  let mediaMetadata = {
    title: props.title,
  };

  if (props.thumbnail) {
    mediaMetadata['artwork'] = [
      { src: props.thumbnail, sizes: '1920x1080', type: 'image/jpeg' },
    ]
  }
  if (props.artist) {
    mediaMetadata['artist'] = props.artist
  }

  let opts = {
    debug: false,
    clickToPlay: true,
    keyboard: { focused: true, global: true },
    controls: [
      'play-large', 'play', 'progress', 'current-time', 'duration', 'mute', 'volume', 'captions', 'settings', 'pip', 'airplay', 'fullscreen'
    ],
    fullscreen: {
      enabled: true,
      fallback: true,
      iosNative: true,
    },
    storage: {
      enabled: true,
      key: 'plyr'
    },
    poster: props.thumbnail,
    artist: props.artist,
    title: props.title,
    mediaMetadata: mediaMetadata,
    captions: {
      update: true,
    }
  };

  if (props.artist) {
    opts.artist = props.artist
  }

  if (props.title) {
    opts.title = props.title
  }

  if (props.thumbnail) {
    opts.poster = props.thumbnail
  }
  player = new Plyr(video.value, opts);

  hls = new Hls({
    debug: false,
    enableWorker: true,
    lowLatencyMode: true,
    backBufferLength: 90,
    fragLoadingTimeOut: 200000,
  });

  hls.loadSource(props.link)

  if (video.value) {
    hls.attachMedia(video.value)
  }

  if (props.title) {
    window.document.title = `YTPTube - Playing: ${props.title}`
  }
}
</script>
