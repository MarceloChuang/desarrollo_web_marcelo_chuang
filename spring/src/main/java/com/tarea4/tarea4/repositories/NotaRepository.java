package com.tarea4.tarea4.repositories;

import com.tarea4.tarea4.models.Nota;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface NotaRepository extends JpaRepository<Nota, Integer> {

    long countByActividadId(Integer actividadId);

    @Query("SELECT AVG(n.valor) FROM Nota n WHERE n.actividad.id = :actividadId")
    Double promedioPorActividad(@Param("actividadId") Integer actividadId);
}