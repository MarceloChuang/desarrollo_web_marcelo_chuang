package com.tarea4.tarea4.repositories;

import com.tarea4.tarea4.models.Actividad;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ActividadRepository extends JpaRepository<Actividad, Integer> {

    @Query("""
        SELECT a
        FROM Actividad a
        JOIN FETCH a.miembro m
        JOIN FETCH m.comuna c
        WHERE LOWER(a.nombre) LIKE LOWER(CONCAT('%', :texto, '%'))
            OR LOWER(a.descripcion) LIKE LOWER(CONCAT('%', :texto, '%'))
            OR LOWER(c.nombre) LIKE LOWER(CONCAT('%', :texto, '%'))
    """)
    List<Actividad> buscarPorTexto(@Param("texto") String texto);
}