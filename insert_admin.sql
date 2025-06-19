
-- SQL para insertar un usuario administrador
INSERT INTO usuarios (nombre, email, password_hash, rol_plataforma, creado_en) 
VALUES (
    'David Marin', 
    'david.marin@example.com', 
    '$2b$12$ePOyVGWDGw3.mXn1fW0X1u/QupX7FVXYcs2YG5Hrks9hV0f9F.VoW', 
    'admin', 
    NOW()
);
