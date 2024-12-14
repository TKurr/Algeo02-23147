import Card from "@/components/audiocard";
import SideBar from "@/components/sidebar";
import UploadMIDI from "@/components/audiosearch";

// export default function Home() {
//   const anjay = {
//     name: "Anjay",
//     artist: "Krisyanto",
//     album: "Anjay",
//     duration: "3:45",
//     image: "/ajay.jpg",
//   }
//   return ( 
//     <main className="bg-gradient-to-b from-[#e0d8ff] from-10% to-blue to-90% flex min-h-screen flex-col items-center">
//       <SideBar />
//       <div className="w-full flex flex-col items-center justify-center">
//         <h1 className="text-[#46404F] text-center w-full text-6xl font-extrabold mb-6">
//           Search by Audio
//         </h1>
//         <div className="gap-4 gap-y-6 mt-12">
//           <AudioCard songs={anjay} />
//         </div>
//       </div>
//     </main>
//   );
// }

export default function Home() {
  return (
    <div>
      <UploadMIDI />
    </div>
  );
}