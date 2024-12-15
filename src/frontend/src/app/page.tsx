import SideBar from "@/components/sidebar";

export default function Home() {
  return ( 
    <main className="flex min-h-screen bg-[#0b0e26]">
      {/* Sidebar */}
      <div className="w-64 bg-white">
        <SideBar />
      </div>
      <div className="w-full flex-1 flex-col items-center justify-center">
        <h1 className="text-white text-center p-6 font-sans text-6xl font-extrabold">
          Home Aja
        </h1>
        <p className="text-white text-center font-sans text-2xl font-semibold">
          Udah Gitu Aja Enjoy :>
        </p>
      </div>
    </main>
  );
}
