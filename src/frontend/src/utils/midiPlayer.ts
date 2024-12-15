import Soundfont from 'soundfont-player';
import MIDIPlayer from 'midi-player-js'

const audioContext = new AudioContext();

export class MidiPlayer {
  private player: any;

  constructor() {
    this.player = new MIDIPlayer.Player();
  }

  playFileFromURL(url: string, onFinish: () => void) {
    fetch(url)
      .then((response) => response.arrayBuffer())
      .then((buffer) => {
        this.player.loadArrayBuffer(buffer);

        // Load a soundfont instrument
        Soundfont.instrument(audioContext, 'acoustic_grand_piano').then((instrument) => {
          this.player.on('midiEvent', (event: any) => {
            if (event.name === 'Note on') {
              instrument.play(event.noteName, audioContext.currentTime, {
                gain: event.velocity / 100,
              });
            }
          });

          this.player.on('endOfFile', onFinish);
          this.player.play();
        });
      })
      .catch((error) => console.error('Error playing MIDI file:', error));
  }

  stop() {
    this.player.stop();
  }
}

export const midiPlayer = new MidiPlayer();
