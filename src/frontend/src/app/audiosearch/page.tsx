import SideBar from "@/components/sidebar";
import UploadMIDI from "@/components/audiosearch";

export default function Home() {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-white">
        <SideBar />
      </div>

      {/* Main Content */}
      <div className="flex-1 bg-[#0b0e26] text-white p-6">
        <UploadMIDI />
      </div>
    </div>
  );
}
