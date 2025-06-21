import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, AlertCircle, CheckCircle, ArrowRight } from 'lucide-react';
import Layout from '../components/Layout';
import { useRouter } from 'next/router';
import { useConfiguratorStore } from '../hooks/useConfiguratorStore';

export default function ImportPage() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [importedConfig, setImportedConfig] = useState<any>(null);
  const router = useRouter();
  const { loadImportedConfiguration } = useConfiguratorStore();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.type === 'application/pdf') {
        setFile(selectedFile);
        setUploadStatus('idle');
        setErrorMessage('');
      } else {
        setErrorMessage('Пожалуйста, выберите PDF файл');
        setUploadStatus('error');
      }
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0];
    if (droppedFile) {
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile);
        setUploadStatus('idle');
        setErrorMessage('');
      } else {
        setErrorMessage('Пожалуйста, выберите PDF файл');
        setUploadStatus('error');
      }
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  const handleImport = async () => {
    if (!file) return;

    setIsUploading(true);
    setUploadStatus('idle');

    try {
      // Создаем FormData для отправки файла
      const formData = new FormData();
      formData.append('file', file);

      // Отправляем файл на сервер
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/configurations/import-pdf`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка импорта');
      }

      const importedData = await response.json();
      
      // Преобразуем данные в нужный формат
      const configData = {
        name: importedData.name,
        components: importedData.components.map((comp: any) => ({
          id: comp.id,
          category: comp.category,
          name: comp.name,
          brand: comp.brand,
          price: comp.price,
          not_found: comp.not_found || false
        })),
        totalPrice: importedData.total_price,
        compatibility_status: importedData.compatibility_status
      };
      
      setImportedConfig(configData);
      setUploadStatus('success');
    } catch (error) {
      console.error('Ошибка импорта:', error);
      setErrorMessage(error instanceof Error ? error.message : 'Ошибка при импорте конфигурации. Проверьте формат файла.');
      setUploadStatus('error');
    } finally {
      setIsUploading(false);
    }
  };

  const handleUseConfiguration = () => {
    // Загружаем импортированную конфигурацию в store
    if (importedConfig) {
      loadImportedConfiguration(importedConfig);
    }
    // Перенаправляем на главную страницу с импортированной конфигурацией
    router.push('/');
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-2xl mx-auto"
          >
            {/* Заголовок */}
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Импорт конфигурации
              </h1>
              <p className="text-gray-600">
                Загрузите PDF файл с сохраненной конфигурацией для восстановления настроек
              </p>
            </div>

            {/* Область загрузки */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl shadow-xl p-8"
            >
              {uploadStatus !== 'success' ? (
                <>
                  {/* Drag & Drop область */}
                  <div
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
                      uploadStatus === 'error' 
                        ? 'border-red-300 bg-red-50' 
                        : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'
                    }`}
                  >
                    {/* Скрытый input для выбора файлов */}
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileSelect}
                      className="hidden"
                      id="file-upload"
                    />
                    
                    <div className="flex flex-col items-center space-y-4">
                      {uploadStatus === 'error' ? (
                        <AlertCircle className="w-16 h-16 text-red-500" />
                      ) : (
                        <Upload className="w-16 h-16 text-gray-400" />
                      )}
                      
                      <div>
                        <p className="text-lg font-medium text-gray-900 mb-2">
                          {file ? file.name : 'Перетащите PDF файл сюда или выберите файл'}
                        </p>
                        <p className="text-sm text-gray-500">
                          Поддерживаются только PDF файлы конфигураций
                        </p>
                      </div>
                                              
                      {!file && (
                          <button 
                            onClick={() => document.getElementById('file-upload')?.click()}
                            className="btn-primary"
                          >
                            Выбрать файл
                          </button>
                        )}

                    </div>
                  </div>

                  {/* Сообщение об ошибке */}
                  {uploadStatus === 'error' && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg"
                    >
                      <div className="flex items-center space-x-2">
                        <AlertCircle className="w-5 h-5 text-red-500" />
                        <p className="text-red-700">{errorMessage}</p>
                      </div>
                    </motion.div>
                  )}

                  {/* Кнопка импорта */}
                  {file && uploadStatus !== 'error' && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="mt-6 text-center"
                    >
                      <button
                        onClick={handleImport}
                        disabled={isUploading}
                        className="btn-primary px-8 py-3 text-lg"
                      >
                        {isUploading ? (
                          <div className="flex items-center space-x-2">
                            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                            <span>Импортируем...</span>
                          </div>
                        ) : (
                          <div className="flex items-center space-x-2">
                            <FileText className="w-5 h-5" />
                            <span>Импортировать конфигурацию</span>
                          </div>
                        )}
                      </button>
                    </motion.div>
                  )}
                </>
              ) : (
                /* Результат импорта */
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="text-center"
                >
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">
                    Конфигурация успешно импортирована!
                  </h3>
                  
                  {importedConfig && (
                    <div className="bg-gray-50 rounded-lg p-6 mb-6 text-left">
                      <h4 className="font-semibold text-gray-900 mb-3">
                        {importedConfig.name}
                      </h4>
                      <div className="space-y-2">
                        {importedConfig.components.map((component: any, index: number) => (
                          <div key={index} className={`flex justify-between items-center p-2 rounded ${
                            component.not_found ? 'bg-yellow-50 border border-yellow-200' : ''
                          }`}>
                            <div className="flex-1">
                              <span className="text-sm text-gray-600">
                                {component.category}: {component.brand} {component.name}
                              </span>
                              {component.not_found && (
                                <div className="text-xs text-yellow-600 mt-1">
                                  ⚠️ Компонент не найден в базе данных
                                </div>
                              )}
                            </div>
                            <span className="text-sm font-medium">
                              {component.price.toLocaleString()} ₽
                            </span>
                          </div>
                        ))}
                      </div>
                      <div className="border-t mt-3 pt-3">
                        <div className="flex justify-between items-center">
                          <span className="font-semibold">Итого:</span>
                          <span className="text-lg font-bold text-green-600">
                            {importedConfig.totalPrice.toLocaleString()} ₽
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  <div className="flex space-x-4">
                    <button
                      onClick={() => {
                        setFile(null);
                        setUploadStatus('idle');
                        setImportedConfig(null);
                      }}
                      className="btn-outline flex-1"
                    >
                      Импортировать другую
                    </button>
                    <button
                      onClick={handleUseConfiguration}
                      className="btn-primary flex-1 flex items-center justify-center space-x-2"
                    >
                      <span>Использовать конфигурацию</span>
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>
                </motion.div>
              )}
            </motion.div>

            {/* Дополнительная информация */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mt-8 text-center"
            >
              <div className="bg-blue-50 rounded-lg p-6">
                <h4 className="font-semibold text-blue-900 mb-2">
                  Как это работает?
                </h4>
                <div className="text-sm text-blue-700 space-y-1">
                  <p>• Загрузите PDF файл с ранее экспортированной конфигурацией</p>
                  <p>• Система автоматически распознает компоненты</p>
                  <p>• Конфигурация будет восстановлена в конфигураторе</p>
                  <p>• Вы сможете продолжить редактирование или сохранить</p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </Layout>
  );
} 