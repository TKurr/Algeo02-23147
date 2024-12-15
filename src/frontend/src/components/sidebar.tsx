'use client';
import { Disclosure, DisclosureButton } from '@headlessui/react';
import React, { useState } from 'react';
import Link from 'next/link';
import { GiHamburgerMenu } from 'react-icons/gi';
import { MdOutlineHome, MdOutlineAudiotrack, MdOutlineImage } from 'react-icons/md';

export default function SideBar() {
  const [files, setFiles] = useState<FileList | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(e.target.files);
    }
  };

  const handleUpload = async (folder: string) => {
    if (!files) {
      alert('Please select files to upload!');
      return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    try {
      const response = await fetch(`http://localhost:5000/upload/${folder}`, {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      alert(result.message);
    } catch (error) {
      console.error('Error uploading files:', error);
      alert('File upload failed!');
    }
  };

  return (
    <div>
      <Disclosure as="nav">
        <DisclosureButton className="absolute top-4 left-4 inline-flex items-center peer justify-center rounded-md p-2 text-gray-900 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white group">
          <GiHamburgerMenu
            className="block md:hidden h-6 w-6"
            aria-hidden="true"
          />
        </DisclosureButton>
        <div className="p-6 w-1/2 h-screen bg-white z-20 fixed top-0 -left-96 lg:w-60 lg:left-0 peer-focus:left-0 peer:transition ease-out delay-150 duration-200">
          <div className="flex flex-col justify-start items-center">
            {/* Dashboard Section */}
            <h1 className="text-base text-center cursor-pointer font-bold text-blue-900 border-b border-gray-100 pb-4 w-full">
              Dashboard
            </h1>
            <div className="my-4 border-b border-gray-100 pb-4">
              <Link href="/">
                <div className="flex mb-2 justify-start items-center gap-4 pl-5 hover:bg-gray-900 p-2 rounded-md group cursor-pointer hover:shadow-lg m-auto">
                  <MdOutlineHome className="text-2xl text-gray-600 group-hover:text-white" />
                  <h3 className="text-base text-gray-800 group-hover:text-white font-semibold">
                    Home
                  </h3>
                </div>
              </Link>
              <Link href="/audiosearch">
                <div className="flex mb-2 justify-start items-center gap-4 pl-5 hover:bg-gray-900 p-2 rounded-md group cursor-pointer hover:shadow-lg m-auto">
                  <MdOutlineAudiotrack className="text-2xl text-gray-600 group-hover:text-white" />
                  <h3 className="text-base text-gray-800 group-hover:text-white font-semibold">
                    Audio Search
                  </h3>
                </div>
              </Link>
              <Link href="/imagesearch">
                <div className="flex mb-2 justify-start items-center gap-4 pl-5 hover:bg-gray-900 p-2 rounded-md group cursor-pointer hover:shadow-lg m-auto">
                  <MdOutlineImage className="text-2xl text-gray-600 group-hover:text-white" />
                  <h3 className="text-base text-gray-800 group-hover:text-white font-semibold">
                    Image Search
                  </h3>
                </div>
              </Link>
            </div>

            {/* Dataset Upload Section */}
            <h1 className="text-base text-center cursor-pointer font-bold text-blue-900 border-b border-gray-100 pb-4 w-full">
              Dataset Upload
            </h1>
            <div className="my-4 border-b border-gray-100 pb-4">
              {/* File Names Display */}
              {files && (
                <div className="mb-4 w-full text-sm text-gray-700">
                  {Array.from(files).map((file, index) => (
                    <p key={index} className="truncate">
                      {file.name}
                    </p>
                  ))}
                </div>
              )}

              {/* Hidden File Input */}
              <input
                type="file"
                multiple
                id="fileInput"
                onChange={handleFileChange}
                className="hidden"
              />

              {/* Styled Label for File Input */}
              <label
                htmlFor="fileInput"
                className="block w-full text-center py-2 px-4 bg-blue-500 text-white font-bold rounded-lg cursor-pointer hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
              >
                Choose Files
              </label>

              {/* Audio Dataset Upload */}
              <div
                onClick={() => handleUpload('midi_dataset')}
                className="flex mt-4 justify-start items-center gap-4 pl-5 hover:bg-gray-900 p-2 rounded-md group cursor-pointer hover:shadow-lg m-auto"
              >
                <MdOutlineAudiotrack className="text-2xl text-gray-600 group-hover:text-white" />
                <h3 className="text-base text-gray-800 group-hover:text-white font-semibold">
                  Upload Audio
                </h3>
              </div>

              {/* Image Dataset Upload */}
              <div
                onClick={() => handleUpload('image_dataset')}
                className="flex mt-4 justify-start items-center gap-4 pl-5 hover:bg-gray-900 p-2 rounded-md group cursor-pointer hover:shadow-lg m-auto"
              >
                <MdOutlineImage className="text-2xl text-gray-600 group-hover:text-white" />
                <h3 className="text-base text-gray-800 group-hover:text-white font-semibold">
                  Upload Image
                </h3>
              </div>
            </div>
          </div>
        </div>
      </Disclosure>
    </div>
  );
}
