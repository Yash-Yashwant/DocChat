import { useState, useCallback } from 'react'
import { Upload, File, X, Check } from 'lucide-react'

const FileUpload = ({ onFileUpload, uploadedFiles }) => {
    const [isDragging, setIsDragging] = useState(false)
    const [uploading, setUploading] = useState(false)

    const handleDrag = useCallback((e) => {
        e.preventDefault()
        e.stopPropagation()
    }, [])

    const handleDragIn = useCallback((e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
            setIsDragging(true)
        }
    }, [])

    const handleDragOut = useCallback((e) => {
        e.preventDefault()
        e.stopPropagation()
        setIsDragging(false)
    }, [])

    const handleDrop = useCallback((e) => {
        e.preventDefault()
        e.stopPropagation()
        setIsDragging(false)

        const files = Array.from(e.dataTransfer.files).filter(
            file => file.type === 'application/pdf'
        )

        if (files.length > 0) {
            handleFiles(files)
        }
    }, [])

    const handleFileInput = (e) => {
        const files = Array.from(e.target.files)
        handleFiles(files)
    }

    const handleFiles = async (files) => {
        setUploading(true)

        try {
            // Upload each file to the backend
            for (const file of files) {
                const formData = new FormData()
                formData.append('file', file)

                const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/upload`, {
                    method: 'POST',
                    body: formData,
                })

                if (!response.ok) {
                    throw new Error('Upload failed')
                }

                const data = await response.json()
                console.log('Upload success:', data)
            }

            onFileUpload(files.map(f => ({
                name: f.name,
                size: f.size,
                uploadedAt: new Date()
            })))
        } catch (error) {
            console.error('Upload error:', error)
            alert('Failed to upload file. Please try again.')
        } finally {
            setUploading(false)
        }
    }

    const removeFile = (index) => {
        // TODO: Implement file removal
        console.log('Remove file:', index)
    }

    return (
        <div className="backdrop-blur-xl bg-white/10 rounded-2xl shadow-2xl p-6 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
                <Upload className="h-6 w-6 text-purple-400" />
                Upload Documents
            </h2>

            {/* Drag and Drop Zone */}
            <div
                className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${isDragging
                    ? 'border-purple-400 bg-purple-500/20 scale-105'
                    : 'border-white/30 hover:border-white/50 bg-white/5'
                    }`}
                onDragEnter={handleDragIn}
                onDragLeave={handleDragOut}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <div className={`transition-transform duration-300 ${isDragging ? 'scale-110' : ''}`}>
                    <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                        <Upload className="h-8 w-8 text-white" />
                    </div>
                    <p className="text-white font-medium mb-2">
                        Drag and drop PDF files here
                    </p>
                    <p className="text-gray-400 text-sm mb-4">or</p>
                    <label className="inline-block">
                        <span className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg cursor-pointer hover:from-purple-600 hover:to-pink-600 transition-all duration-300 shadow-lg hover:shadow-purple-500/50 font-medium">
                            Browse Files
                        </span>
                        <input
                            type="file"
                            className="hidden"
                            accept=".pdf"
                            multiple
                            onChange={handleFileInput}
                        />
                    </label>
                </div>
            </div>

            {/* Uploaded Files List */}
            {uploadedFiles.length > 0 && (
                <div className="mt-6">
                    <h3 className="text-sm font-semibold text-gray-300 mb-3 flex items-center gap-2">
                        <Check className="h-4 w-4 text-green-400" />
                        Uploaded Files ({uploadedFiles.length})
                    </h3>
                    <div className="space-y-2">
                        {uploadedFiles.map((file, index) => (
                            <div
                                key={index}
                                className="flex items-center justify-between p-4 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 hover:bg-white/10 transition-all duration-300 group"
                            >
                                <div className="flex items-center space-x-3 flex-1 min-w-0">
                                    <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                                        <File className="h-5 w-5 text-white" />
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-sm font-medium text-white truncate">{file.name}</p>
                                        <p className="text-xs text-gray-400">
                                            {(file.size / 1024).toFixed(2)} KB
                                        </p>
                                    </div>
                                </div>
                                <button
                                    onClick={() => removeFile(index)}
                                    className="flex-shrink-0 ml-2 p-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all duration-300 opacity-0 group-hover:opacity-100"
                                >
                                    <X className="h-5 w-5" />
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {uploading && (
                <div className="mt-4 text-center">
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-500/20 rounded-lg border border-purple-500/30">
                        <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin"></div>
                        <span className="text-sm text-purple-300 font-medium">Uploading...</span>
                    </div>
                </div>
            )}
        </div>
    )
}

export default FileUpload
