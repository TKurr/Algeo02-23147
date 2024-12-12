import {AudioCard} from "../components/audiocard";
import AudioSearcher from "../components/audiosearcher";

export default function Home() {
  return (  
    <App />
  );
}

const MainContent = () => {
  return (
      <div className="w-4/6 p-2">
          <div className="flex justify-center mb-4">
              <button className="bg-gray-700 hover:bg-gray-800 text-white py-2 px-4 rounded-l-lg">Album</button>
              <button className="bg-white text-blue-900 py-2 px-4 rounded-r-lg">Music</button>
          </div>
          <div className="grid grid-cols-3 gap-4">
              {Array.from({ length: 6 }).map((_, index) => (
                  <AudioCard key={index} index={index} />
              ))}
          </div>
      </div>
  );
};

const App = () => {
  return (
    <section className="bg-bannerImg bg-repeat bg-cover bg-bottom">
          <div className="w-full flex bg-blackOverlay">
              <AudioSearcher />
          </div>
    </section>
  );  
};
